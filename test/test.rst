Hello World!
============

This is an example of reference to field |cron_user| and its help |cron_user_help|. This one is an example of a menu entry: |menu_name| while this one is a reference to a complete entry: |menu_complete_name|.

.. |cron_user| field:: ir.cron/user

.. |cron_user_help| field:: ir.cron/user
   :help:

.. |menu_name| tryref:: ir.menu_cron_form/name

.. |menu_complete_name| tryref:: ir.menu_cron_form/complete_name

.. view:: party.party_party_form
   :field: name

This is an example of a field reference in the text: *@field:ir.cron/user@*, while this one is an example of a menu entry in the text: *@tryref:ir.menu_cron_form/complete_name@*.

And now, the same example of field with help option: *@field:ir.cron/user:help@*.

