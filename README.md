<p align="center">
<img src="cryptians.png"></a>
</p>

## Getting Started

For Linux or MacOS use **pip3 and python3**

### Step 1: Clone the project to your local directory

Open the Terminal and use command:

    git clone https://github.com/mark47546/Cryptians.git

### Step 2: Go to the project directory

    cd Cryptians/cryptians/

### Step 3: Create new enviroment in this directory

Create .env file by copy data from the env.example
or
Rename env.example to .env

### Step 4: Open Docker app

Open the Docker appication in your machine

### Step 5: Run Docker compose

    cd ..

    docker-compose up -d
    
### Step 6: Open your browser and open localhost:8000

Open your browser and redirect url to localhost port 8000


### To create a super user: Open Docker CLI
<p align="center">
<img src="docker_cli.png"></a>
</p>
Open Docker CLI and run command:

    python manage.py createsuperuser
          
