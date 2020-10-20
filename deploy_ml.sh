cd models_and_data
git pull
cd ..

mv ./models_list.json /app/web_app/models_list.json
touch /app/web_app/main.py

if [ $? -eq 0 ]; then
  echo "Model successfully deployed"
else
  echo "Error while deploying model. Check web app logs"
fi

