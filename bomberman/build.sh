docker build -t aperence/bomberman-game-server ./frontend
docker build -t aperence/bomberman ./server
docker build -t aperence/db-bomberman ./db
docker build -t aperence/bomberman-cleaning ./cleaner
docker push aperence/bomberman
docker push aperence/bomberman-game-server
docker push aperence/db-bomberman 
docker push aperence/bomberman-cleaning