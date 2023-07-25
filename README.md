# knative function in local

## 1. 클러스터 구축
간편한 구축을 위해 **kind**와 **Knative quickstart plugin**을 이용
```bash
# knative용 클러스터 구축
kind create cluster --name knative --image kindest/node:v1.23.5

# knative 클러스터 컨텍스트 사용
kubectl config use-context kind-knative
```
## 2. knative 플러그인 설치

```bash
# 맥의 경우
brew install knative-sandbox/kn-plugins/quickstart

kn quickstart kind
```

## 3. knative function

```bash
func create -l python <function name>
```

아래의 파일 수정해야함
- func.py
- requirements.txt

```
func build
func deploy
```