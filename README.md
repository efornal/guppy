# guppy
Coordinate system that allows integration between different projects.
Each project has a responsibility assigned and is responsible for reporting changes in their projects. When a change for a particular project is added, the system notifies all responsible for projects that are 'integrated' with the project on which the change was applied.
Also, each manager can see notifications about changes applied to different projects and indicate acceptance or disagreement with each change.
This way you can keep track of the various changes affecting projects that make integration and to determine the conformity of the respective responsible.


### Package Installation debian stretch
```bash
sudo apt-get install python-dev
sudo apt-get install python-pip
sudo apt-get install libpq-dev
sudo apt-get install libyaml-dev
sudo apt-get install libldap2-dev
sudo apt-get install libsasl2-dev
sudo apt-get install gettext
sudo apt-get install libjpeg-dev
sudo apt-get install zlib1g-dev
sudo apt-get install python-dnspython # for reidi
sudo apt-get install mariadb-client # for dumpserver
sudo apt-get install pkg-config
sudo apt-get install libgtk2.0-dev
sudo apt-get install libgirepository1.0-dev
```

### Python lib Installation
```bash
pip install -r requirements.txt
```
