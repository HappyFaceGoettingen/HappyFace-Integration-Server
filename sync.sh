#!/bin/sh

rsync -avzl --delete -e "ssh -p 24" ../HappyFace-Integration-Server/* login.ph2:public_html/happyface/
