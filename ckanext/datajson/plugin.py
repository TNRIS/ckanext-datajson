import re

import ckan.plugins as p

from . import blueprint


class DataJsonPlugin(p.SingletonPlugin):
    p.implements(p.interfaces.IConfigurer)
    p.implements(p.ITemplateHelpers)
    p.implements(p.interfaces.IRoutes, inherit=True)
    p.implements(p.IBlueprint)

    def update_config(self, config):
        # Must use IConfigurer rather than IConfigurable because only IConfigurer
        # is called before after_map, in which we need the configuration directives
        # to know how to set the paths.

        # TODO commenting out enterprise data inventory for right now
        # DataJsonPlugin.route_edata_path = config.get("ckanext.enterprisedatajson.path", "/enterprisedata.json")
        DataJsonPlugin.route_enabled = config.get("ckanext.datajson.url_enabled", "True") == "True"
        DataJsonPlugin.route_path = config.get("ckanext.datajson.path", "/data.json")
        DataJsonPlugin.route_ld_path = config.get("ckanext.datajsonld.path",
                                                  re.sub(r"\.json$", ".jsonld", DataJsonPlugin.route_path))
        DataJsonPlugin.ld_id = config.get("ckanext.datajsonld.id", config.get("ckan.site_url"))
        DataJsonPlugin.ld_title = config.get("ckan.site_title", "Catalog")
        DataJsonPlugin.export_map_filename = config.get("ckanext.datajson.export_map_filename", "export.map.json")
        DataJsonPlugin.site_url = config.get("ckan.site_url")

        DataJsonPlugin.inventory_links_enabled = config.get("ckanext.datajson.inventory_links_enabled",
                                                            "False") == "True"

        # Adds our local templates directory. It's smart. It knows it's
        # relative to the path of *this* file. Wow.
        p.toolkit.add_template_directory(config, "templates")

    @staticmethod
    def datajson_inventory_links_enabled():
        return DataJsonPlugin.inventory_links_enabled

    def get_helpers(self):
        return {
            "datajson_inventory_links_enabled": self.datajson_inventory_links_enabled
        }

    def get_blueprint(self):
        return blueprint.datapusher
