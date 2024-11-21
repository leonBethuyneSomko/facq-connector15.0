FROM docker.somko.be/odoo/enterprise:14.0_20230124
USER root

ADD requirements.txt /
RUN pip3 install -r /requirements.txt

COPY custom /mnt/repo/custom
COPY third /mnt/repo/third

USER odoo
