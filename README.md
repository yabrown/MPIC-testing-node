# README 

## Overview 
This codebase automatically deploys a Docker container running a Flask app to Vultr VMs. If the image is updated, the codebase will automatically pull and run the new image. 

## Docker Configuration on Local Machine  
1. **Get Docker Desktop**
    - This is necessary to build images, run containers, and more. 
2. **Create a new Docker Hub image repository**
    - In this example, I named the repository as "docker-tutorial"
3.  **Clone this repository to your local machine**
4.  **Build and push image using following command**
    - Remember to replace the following entries with your own information
    - Feel free to edit the Flask app to implement your own application before building 
    - OPTIONAL: using --platform flag, I built the image so that it can run on various architectures 
      ```bash
        docker buildx build --platform linux/amd64,linux/arm64 --push -t [DOCKER-USERNAME]/[DOCKER-REPO]:[TAG] .
      ```

## Deploy Container on Vultr VM
1.  **Add startup script to Vultr account**
     - (No need to add again, if you're using this script since it's already on our account)
2.  **Deploy new VM**
     - Please note that startup scripts are only run once (when the VM is first provisioned)
     - If you want to add this startup script to a VM auto-deployment in terraform, add "script_id" to your vultr_instance resource (you can get the ID from the startup script url)
3.  **App is now deployed!**
     - To test out this app in particular, run
       ```bash
        curl [VM_url]:5000 
       ```
     - If you want to change how frequently watchtower monitors for new images, edit the --interval flag in vultr-startup-script.sh (it is currently set to monitor and pull new images every 30 seconds)
