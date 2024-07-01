# youflask
A simple flask server to download and view videos from youtube to your own computer.</br>
You can also rename, delete or download the videos to your device.</br>

This project was made to learn how to run a service on a kubernetes kluster with NFS storage.</br>
</br>
It ran successfully on a kubernetes kluster with one master node and two worker nodes.</br>
In my case it was enough to have 2 replicas, one on each worker.</br>
Each node is running on a virtual client on a proxmox server but the NFS server is runnning on a Raspberry Pi.</br>
</br>
The part concerning the NFS is at the end of the *deployment.yml* file where the mountpoint in the pod is specified *(volumeMounts:)* and the NFS servers IP and path is specified *(volumes:)*.</br>
</br>
I've included the Dockerfile and deployment.yml I used but with some information removed:


#### Dockerfile:
<pre>
FROM python:3.10.12
RUN mkdir /app
WORKDIR /app/
ADD . /app/
RUN pip install -r requirements.txt
CMD ["python", "/app/app.py"]
</pre>

#### deployment.yml
<pre>
apiVersion: v1
kind: Service
metadata:
  name: youflask-service
spec:
  selector:
    app: youflask-app
  ports:
    - protocol: "TCP"
      port: 6000
      targetPort: 5000
  type: LoadBalancer

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: youflask-app
spec:
  selector:
    matchLabels:
      app: youflask-app
  replicas: 2
  template:
    metadata:
      labels:
        app: youflask-app
    spec:
      containers:
        - name: youflask-app
          image: docker.io/userID/dockerImageName:tag
          imagePullPolicy: IfNotPresent
          ports:
            - containerPort: 5000
          volumeMounts:
            - name: nfs-vol
              mountPath: /app/download
      volumes:
        - name: nfs-vol
          nfs:
            server: ip.addr.to.NFS.server
            path: /mnt/path/to/shared/NFS/folder
</pre>
