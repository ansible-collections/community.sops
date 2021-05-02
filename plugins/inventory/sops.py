import os
from tempfile import NamedTemporaryFile

from ansible.errors import AnsibleParserError
from ansible.plugins.inventory import BaseInventoryPlugin
from ansible.plugins.loader import inventory_loader


from ansible_collections.community.sops.plugins.module_utils.sops import Sops


class InventoryModule(BaseInventoryPlugin):

    NAME = 'sops'
    PATH_ENDINGS = (
        '.sops.yml',
        '.sops.yaml',
        '.sops.json',
    )

    def verify_file(self, path):
        if not any(path.endswith(ending) for ending in self.PATH_ENDINGS):
            return False
        return super(InventoryModule, self).verify_file(path)

    def parse(self, inventory, loader, path, cache=True):
        plugin_name = self._plugin_name_from_path(path)
        plugin = inventory_loader.get(plugin_name)
        if not plugin:
            raise AnsibleParserError("sops requires the plugin {!r} to be enabled because of this file {!r}".format(plugin_name, path))
        temporary = NamedTemporaryFile(mode='w', suffix=os.path.basename(path), delete=False)
        with temporary as f:
            f.write(Sops.decrypt(path))

        try:
            self._parse(plugin, inventory, loader, temporary.name, cache=cache)
        finally:
            os.unlink(temporary.name)

    def _parse(self, plugin, inventory, loader, path, cache=True):
        plugin.parse(inventory, loader, path, cache=cache)

        try:
            plugin.update_cache_if_changed()
        except AttributeError:
            pass

    @staticmethod
    def _plugin_name_from_path(path):
        (_, extension) = os.path.splitext(path)
        clean_extension = extension[1:]
        extension_mapping = {
            "yml": "yaml"
        }
        # If an invalid extension is sent, let the parser validate
        return extension_mapping.get(clean_extension, clean_extension)