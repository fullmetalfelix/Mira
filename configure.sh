#!/bin/bash

echo "configuring AMAD local server..."
echo "current folder:"
pwd

echo "compiling AMAD documentation..."
rm -rf ./docs/* ./docs-build
cp -r ./docs-common ./docs-build

# copy definitions
cp ./docs-amad/defs.rst ./docs-build/.

# copy the logo/images
cp -r ./docs-amad/_static/* ./docs-build/_static/.


for type in generic data proc vis 
do
	for module in cassandra amad 
	do
		FILE=module-${module}-${type}.rst
		if test -f "./docs-${module}/steps/$FILE"; then
			echo "$FILE exists" 
			cp ./docs-${module}/steps/${FILE} ./docs-build/steps/.
			sed -i "s/.. STEPS-${type}/.. include:: \/steps\/${FILE}\n.. STEPS-${type}/g" ./docs-build/notebooks.rst
		else
			echo "$FILE not found"
		fi
	done
done
sphinx-build -b html ./docs-build ./docs

# --- DOCUMENTATION DONE --- #


echo "creating setup files..."
cp setup/amad-local/app.py .
cp setup/amad-local/config.py .
cp setup/amad-local/routes.py .

# copy icons
cp amad/static/imgs/*.logo.svg static/imgs/.
cp amad/static/imgs/*.user.*.svg static/imgs/.

# make a global template-main
mkdir templates

cp core/templates/* templates/.
cp core/*/templates/* templates/.
cp core/templates-main/* templates/.

cp cassandra/templates/* templates/.

cp amad/templates/* templates/.
cp amad/*/templates/* templates/.
cp amad/templates-main/* templates/.


# setup common routes
sed -i '/FLAG_COMMON_ROUTES/ r common-routes.py' app.py


echo "configuration completed"
