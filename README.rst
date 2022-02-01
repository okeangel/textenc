
TODO
====

1. Measure estimated finish time. If time is more than N=10m then alert milestones. Use sound and messages (telegram?) alerts.

2. Run Telegram service on Windows startup. Connect to Telegram account. Wait for commands. Examples of commands^: 

3. Опубликовать проект в PyPI.

4. Подсчёт:
 - сколько CRLF
 - сколько осталось LFCR
 - сколько осталось CR
 - сколько осталось LF

5. Сколько байт. Сколько символов.

6. Расставь правила замен.
RS - на дефис
Все NULL - на один CRLF
Если IBM 866 и ў - заменить на ё.
\r\n\f\r\n *- [0-9]* -\r\n\r\n на \r\n при IBM 866
\r\n *[0-9]*\r\n\f\r\n на \r\n при IBM 866
\r\n\f\r\n на \r\n при IBM 866

7. SPSP - замена на SPSP, пока не останется замен.
NBSPNBSP - то же самое.

SP.SP - на .SP

SPCRLF - на CRLF, повторять пока не останется замен.



