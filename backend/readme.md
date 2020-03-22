  
# start using docker

please note: not tested, contribute here if you have findings.

     docker image build -t covidqa .
     docker run --publish 8000:8080  covidqa


# Run locally on mac os

make sure python3 is installed. In my case it's pip3 / python3 
    
    pip3 install virtualenv
    virtualenv venv  
    source venv/bin/activate
    cd ..  
    pip install -r requirements.txt
    
    brew tap elastic/tap
    brew install elastic/tap/elasticsearch-full
    elasticsearch
    
    uvicorn backend.api:app
    
