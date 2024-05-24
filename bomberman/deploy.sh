kubectl delete -f db/k8s 2> /dev/null || true
kubectl delete -f server/k8s 2> /dev/null || true
kubectl apply -f db/k8s
kubectl apply -f server/k8s