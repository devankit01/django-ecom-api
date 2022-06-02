# A database Router is a class that provides up to four methods

class AuthRouter:
    """A router to control all database operations on models in the
     applications"""
    #django.contrib.admin as admin
    route_app_labels={'auth','contenttypes','sessions','admin','sessions'} #router_app_labels contains the apps which is defining in the installed apps and then all above operations perform on it.

    """ Attempts to read  app models """
    def db_for_read(self,model,**hints):
        if model._meta.app_label in self.route_app_labels:
            return 'default'
        return None


    """ Attempts to write app models"""
    def db_for_write(self,model,**hints):
        if model._meta.app_label in self.route_app_labels:
            return 'default'
        return None

    """ Allow relations  if models in the app """
    def allow_relation(self,obj1,obj2,**hints):
        if (
            obj1._meta.app_label in self.route_app_labels or 
            obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None


    def allow_migrate(self,db,app_label,model_name=None,**hints):
        """ Make sure the your apps only appear in the
        'users_db' database."""

        if app_label in self.route_app_labels:
            return db == "default"
        return None