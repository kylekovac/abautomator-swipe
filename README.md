# abautomator
A/B testing at the press of a button

## Setup

Via docker (recommended):

```bash
docker build -t abauto . && docker run -it --rm -v ${PWD}:/transformations make-seg
```

Or within a `virtualenv` run the standard

```bash
pip install -r requirements.txt
```
