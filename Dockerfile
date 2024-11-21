FROM docker.somko.be/odoo/enterprise:13.0_20221118
USER root

ADD requirements.txt /
RUN pip3 install -r /requirements.txt

COPY custom /mnt/repo/custom
COPY third /mnt/repo/third

USER odoo
