Install
=========

This is where you write how to get a new laptop to run this project.

Create the local postgresql database::

    createdb lettoo_weixin_platform

    createuser lettoo -P

    psql lettoo_weixin_platform

    psql> GRANT ALL PRIVILEGES ON DATABASE lettoo_weixin_platform TO lettoo;

