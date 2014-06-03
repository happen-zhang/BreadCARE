#-*- coding: UTF-8 -*-
import json
import tornado.web

class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        try:
            return eval(self.get_secure_cookie('user_data'))
        except:
            return False

    def load_json(self):
        try:
            self.request.arguments = json.loads(self.request.body)
        except ValueError:
            msg = 'Could not decode JSON: %s' % self.request.body
            logger.debug(msg)
            raise tornado.web.HTTPError(400, msg)

    def get_json_argument(self, name, default = None):
        if default is None:
            default = self._ARG_DEFAULT
        if not self.request.arguments:
            self.load_json()
        if name not in self.request.arguments:
            if default is self._ARG_DEFAULT:
                msg = "Missing argument '%s'" % name
                logger.debug(msg)
                raise tornado.web.HTTPError(400, msg)
            logger.debug("Returning default argument %s, as we couldn't find "
                    "'%s' in %s" % (default, name, self.request.arguments))
            return default
        arg = self.request.arguments[name]
        logger.debug("Found '%s': %s in JSON arguments" % (name, arg))
        return arg

    def wdb( self ):
        # write database
        try:
            return self.db_links[ 'wdb' ]
        except Exception, e:
            from tornado import database
            import settings
            db_links = database.Connection('%s:%s' % 
                (
                    settings.database_config[ 'wdb' ][ 'host' ],
                    int( settings.database_config[ 'wdb' ][ 'port' ] )
                ),
                settings.database_config[ 'wdb' ][ 'dbnm' ],
                settings.database_config[ 'wdb' ][ 'user' ],
                settings.database_config[ 'wdb' ][ 'pswd' ],
                max_idle_time = 15,
            )
            try:
                self.db_links[ 'wdb' ] = db_links
            except Exception, e:
                self.db_links = {}
                self.db_links[ 'wdb' ] = db_links
            return db_links
    def rdb( self ):
        # read database
        try:
            settings.database_config[ 'rdb' ]
        except Exception, e:
            return self.wdb()
        try:
            return self.db_links[ 'rdb' ]
        except Exception, e:
            import settings
            rdbconfig = settings.database_config[ 'rdb' ]
            if len( rdbconfig ):
                from tornado import database
                import random
                dbconfig = rdbconfig #random.choice( rdbconfig )
                db_links = database.Connection('%s:%s' % 
                    (
                        dbconfig[ 'host' ],
                        int( dbconfig[ 'port' ] )
                    ),
                    dbconfig[ 'dbnm' ],
                    dbconfig[ 'user' ],
                    dbconfig[ 'pswd' ],
                    max_idle_time = 15,
                )
            else:
                return self.wdb()