import tornado
import tornado.template
import os
from tornado.options import define, options

path = lambda root, *a: os.path.join(root, *a)
ROOT = os.path.dirname(os.path.abspath(__file__))

define('port', default = 8001, help = 'run on the given port', type = int)
define('config', default = None, help = 'tornado config file')
define('debug', default = True, help = 'debug mode')
database_config = {
    # master
    'wdb' : {
        'host' : 'rdsii3uvuii3uvu.mysql.rds.aliyuncs.com',
        'port' : '3306',
        'user' : 'db3mfdjdaeg5c0j6',
        'pswd' : '123456asd',
        'dbnm' : 'db3mfdjdaeg5c0j6'
    },

    # slaves
#    'rdb' : (
#
#        {
#            'host' : 'localhost',
#            'port' : '3306',
#            'user' : 'root',
#            'pswd' : 'root',
#            'dbnm' : 'breadcare'
#        }
#
#    )

    }
tornado.options.parse_command_line()

STATIC_ROOT = path(ROOT, 'static' )
TEMPLATE_ROOT = path(ROOT, 'templates')

# Deployment Configuration
class DeploymentType:
    PRODUCTION = 'PRODUCTION'
    DEV = 'DEV'
    SOLO = 'SOLO'
    STAGING = 'STAGING'
    dict = {
        SOLO: 1,
        PRODUCTION: 2,
        DEV: 3,
        STAGING: 4
    }

if 'DEPLOYMENT_TYPE' in os.environ:
    DEPLOYMENT = os.environ['DEPLOYMENT_TYPE'].upper()
else:
    DEPLOYMENT = DeploymentType.SOLO

settings = {}
settings['debug'] = DEPLOYMENT != DeploymentType.PRODUCTION or options.debug
settings['static_path'] = STATIC_ROOT
settings['cookie_secret'] = 'set_you_secury_cookie'
settings['xsrf_cookies'] = True
settings['template_loader'] = tornado.template.Loader(TEMPLATE_ROOT)
settings['login_url'] = '/$login'

if options.config:
    tornado.options.parse_config_file(options.config)
