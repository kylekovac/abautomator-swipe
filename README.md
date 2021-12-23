# abautomator
A/B testing at the press of a button

<<<<<<< HEAD

### Setup

```bash
gcloud auth login
gcloud auth application-default login

docker build -t abauto .
docker run -ti --rm \
    -v ${PWD}:/abautomator ab-venv                # mount repo to volume
    -v=$HOME/.config/gcloud:/root/.config/gcloud  # mount gcloud cred to vol
```
