
from subprocess import call

print '**** starting ***'

SETTINGS_FILE= 'promedic.settings_prod'
# SETTINGS_FILE= 'promedic.settings'

call(['python', 'manage.py', 'makemigrations', '--settings=%s'% SETTINGS_FILE])
call(['python', 'manage.py', 'migrate', '--settings=%s'% SETTINGS_FILE])


call(['python', 'manage.py', 'loaddata', 'core/fixtures/allergies.json', '--settings=%s'% SETTINGS_FILE])
call(['python', 'manage.py', 'loaddata', 'core/fixtures/blood_group.json', '--settings=%s'% SETTINGS_FILE])
call(['python', 'manage.py', 'loaddata', 'core/fixtures/disabilities.json', '--settings=%s'% SETTINGS_FILE])
call(['python', 'manage.py', 'loaddata', 'core/fixtures/drug-forms.json', '--settings=%s'% SETTINGS_FILE])
call(['python', 'manage.py', 'loaddata', 'core/fixtures/drug-brands.json', '--settings=%s'% SETTINGS_FILE])
call(['python', 'manage.py', 'loaddata', 'core/fixtures/dispense-types.json', '--settings=%s'% SETTINGS_FILE])
call(['python', 'manage.py', 'loaddata', 'core/fixtures/genotypes.json', '--settings=%s'% SETTINGS_FILE])
call(['python', 'manage.py', 'loaddata', 'core/fixtures/states.json', '--settings=%s'% SETTINGS_FILE])
call(['python', 'manage.py', 'loaddata', 'core/fixtures/local_govt.json', '--settings=%s'% SETTINGS_FILE])
call(['python', 'manage.py', 'loaddata', 'core/fixtures/equipments.json', '--settings=%s'% SETTINGS_FILE])
call(['python', 'manage.py', 'loaddata', 'core/fixtures/area-of-concentration.json', '--settings=%s'% SETTINGS_FILE])
call(['python', 'manage.py', 'loaddata', 'core/fixtures/kits.json', '--settings=%s'% SETTINGS_FILE])
call(['python', 'manage.py', 'loaddata', 'core/fixtures/doc-type.json', '--settings=%s'% SETTINGS_FILE])
call(['python', 'manage.py', 'loaddata', 'core/fixtures/gender.json', '--settings=%s'% SETTINGS_FILE])
call(['python', 'manage.py', 'loaddata', 'core/fixtures/users.json', '--settings=%s'% SETTINGS_FILE])
call(['python', 'manage.py', 'loaddata', 'core/fixtures/side-effects.json', '--settings=%s'% SETTINGS_FILE])
call(['python', 'manage.py', 'loaddata', 'core/fixtures/drug-contraindications.json', '--settings=%s'% SETTINGS_FILE])
call(['python', 'manage.py', 'loaddata', 'core/fixtures/drug-indications.json', '--settings=%s'% SETTINGS_FILE])
call(['python', 'manage.py', 'loaddata', 'core/fixtures/drug-classifications.json', '--settings=%s'% SETTINGS_FILE])
call(['python', 'manage.py', 'loaddata', 'core/fixtures/hmos.json', '--settings=%s'% SETTINGS_FILE])