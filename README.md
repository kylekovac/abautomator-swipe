# abautomator
A/B testing at the press of a button


### Setup

Development:

```bash
# Should only keep to run these gcloud commands once
gcloud auth login
gcloud auth application-default login

docker build -t abauto .
docker run -ti --rm                                \
    -v ${PWD}:/abautomator ab-venv                 \  # mount repo to volume
    -v=$HOME/.config/gcloud:/root/.config/gcloud   \  # mount gcloud cred to vol
    abauto
```

Jupyter

```
docker run -p 8888:8888                    \
    -v ${PWD}:/home/jovyan/work            \
    jupyter/scipy-notebook:33add21fab64 
```
