 docker stop movie;
docker rm movie;
docker stop movie; 
docker rm movie;
docker build -t movie .;
docker run -p 5001:5001 --restart=always -d --name=movie movie;