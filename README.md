# SDLE Second Assignment

SDLE Second Assignment of group T02;G11.

Group members:

1. [Duarte Sardão](https://github.com/duarte-sardao)
2. [Henrique Sousa (Self)](https://github.com/henriquecscode)
3. [Mateus Silva](https://github.com/lessthelonely) 
4. [Melissa Silva](https://github.com/melisilva)

## How To Compile

### Pre-requisites
To compile this project it's necessary to have the Kademlia library for Python; Fastapi and Node.js installed in your machine.

To install the Kademlia library, please execute the following command in your terminal:
```bash
pip install kademlia 
```

For Fastapi:
```bash
pip install "fastapi[all]"
```

To install Node.js, please download it from the official website in the following link: https://nodejs.org/en/download/

### Running
This project has 3 parts:

#### Bootstrap
To compile and run this part, the following commands should be executed:
```bash
cd src/backend/src
python static.py
```

To start the peers, execute:
```bash
cd src/backend/src
python main.py ID # ID is numeric
```
The above commands can be executed in multiple terminal windows, to have as many peers as the user wishes.

To start the frontend, execute:
```bash
cd src/frontend/src
npm i
npm run build
npm run dev
```





