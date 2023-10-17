# shadow-analysis
shadow-analysis


Building docker:
docker image build -t shadow-analyzer .

To create Container:
docker create -p 5000:5000 shadow-analyzer

Start Container:
docker start <container-id>

Create and start container:
docker run -p 5000:5000 -d shadow-analyzer