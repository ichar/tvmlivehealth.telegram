# -*- coding: utf-8 -*-

import re
import time
from copy import deepcopy
import random

from config import (
     IsDebug, IsDeepDebug, IsTrace, IsPrintExceptions, IsWithPrintErrors, IsWithGroup, IsWithExtra,
     errorlog, print_to, print_exception,
    )

from app.settings import DEFAULT_LANGUAGE, DEFAULT_PARSE_MODE, NO_RESULTS, RCODES
from app.dialogs.start import help
from app.handlers import *

from app import dbs

# Группировка результатов
_with_group = IsWithGroup
# Ответ "Не знаю"
_with_extra = IsWithExtra

# Финальный результат теста
_is_without_conclusions = 0

# -------------------------------------
# Тест на эмоциональное выгорание Бойко
# -------------------------------------

_TEST_NAME = 'T11'
_QCOUNT = 84

_QUESTIONS = {
    'ru': (
"""
1. Организационные ошибки на работе постоянно заставляют меня нервничать, напрягаться, волноваться
""",
"""
2. Сегодня я доволен своей профессией не менее, чем в начале своей карьеры
""",
"""
3. Я ошибся в выборе профессии или профиле деятельности (занимаю не своё место)
""",
"""
4. Меня беспокоит то, что я стал хуже работать (менее производительно, менее качественно, медленнее)
""",
"""
5. Тепло во взаимодействии с партнёрами очень зависит от моего настроения
""",
"""
6. От меня как профессионала мало зависит благосостояние партнёров
""",
"""
7. Когда я прихожу с работы домой, то некоторое время (часа 2-3) мне хочется побыть в одиночестве, чтобы со мной никто не общался
""",
"""
8. Когда я ощущаю усталость или напряжение, то стараюсь побыстрее решить проблемы партнёра (свернуть взаимодействие)
""",
"""
9. Мне кажется, что эмоционально я не могу дать коллегам того, что требуют профессиональные обязанности
""",
"""
10. Моя работа притупляет эмоции
""",
"""
11. Я откровенно устал от человеческих проблем, с которым приходится иметь дело по работе
""",
"""
12. Случается, что я иногда плохо засыпаю (сплю) из-за беспокойства, связанного с работой
""",
"""
13. Взаимодействие с партнёрами требует от меня большого напряжения
""",
"""
14. Работа с людьми приносит мне всё меньше удовлетворения
""",
"""
15. Я бы сменил место работы, если бы появилась такая возможность
""",
"""
16. Меня часто расстраивает то, что я не могу на необходимом уровне предоставить профессиональную поддержку, услугу, помощь
""",
"""
17. Мне всегда удаётся предотвратить влияние плохого настроения на деловые контакты
""",
"""
18. Меня очень расстраивает ситуация, когда что-то идёт не так в отношениях с деловым партнёром
""",
"""
19. Я так устаю на работе, что дома стараюсь общаться как можно меньше
""",
"""
20. Из-за нехватки времени, усталость и напряжение я часто уделяю партнёру меньше времени, чем надо
""",
"""
21. Иногда обычные ситуации общения на работе раздражают меня
""",
"""
22. Я спокойно воспринимаю обоснованные претензии партнёров
""",
"""
23. Общение с партнёрами вынуждает меня избегать людей
""",
"""
24. При упоминании о некоторых партнёрах и коллегах у меня портится настроение
""",
"""
25. Конфликты и споры с коллегами отнимают много сил и эмоций
""",
"""
26. Мне всё сложнее устанавливать или поддерживать контакты с деловыми партнёрами
""",
"""
27. Обстоятельства на работе мне кажутся очень сложными и тяжёлыми
""",
"""
28. У меня часто возникают тревожные ожидания, связанные с работой: что-то должно случиться, как бы не допустить ошибку, смогу ли я сделать всё, что надо, не сократят ли меня и др
""",
"""
29. Если партнёр мне неприятен, я стараюсь ограничить время общения с ним, меньше уделять ему внимания
""",
"""
30. В общении на работе я придерживаюсь принципа «не делай людям добро – не получишь зло»
""",
"""
31. Я с радостью рассказываю домашним о своей работе
""",
"""
32. Случаются дни, когда моё эмоциональное состояние плохо отражается на результатах работы (меньше работаю, снижается качество, возникают конфликты)
""",
"""
33. Иногда я чувствую, что нужно посочувствовать партнёру, но я не способен этого сделать
""",
"""
34. Я очень волнуюсь за свою работу
""",
"""
35. Партнёрам по работе уделяю больше внимания и заботы, нежели получаю от них благодарности
""",
"""
36. При одном упоминании о работе мне становится плохо: начинает колоть в области сердца, повышается давление, возникает головная боль
""",
"""
37. У меня хорошие (в целом удовлетворительные) отношения с непосредственным руководителем
""",
"""
38. Я часто радуюсь, когда вижу, что моя работа приносит пользу людям
""",
"""
39. В последнее время меня преследуют неудачи на работе
""",
"""
40. Некоторые аспекты (факты) моей работы вызывают разочарование, скуку и разочарование
""",
"""
41. Случаются дни, когда контакты с партнёрами складываются хуже, чем обычно
""",
"""
42. Я переживаю о проблемах деловых партнёров (субъектов деятельности) меньше, чем обычно
""",
"""
43. Усталость от работы приводит к тому, что я стараюсь сократить время общения с друзьями и знакомыми
""",
"""
44. Обычно я проявляю интерес к личности партнёра больший, нежели того требует дело
""",
"""
45. Обычно я прихожу на работу отдохнувшим, со свежими силами, в хорошем настроении
""",
"""
46. Иногда я ловлю себя на том, что работаю с партнёрами автоматически, без души
""",
"""
47. В делах встречаются настолько неприятные люди, что вопреки воле желаешь им чего-то нехорошего
""",
"""
48. После общения с неприятными партнёрами у меня бывает ухудшение физического и психического самочувствия
""",
"""
49. На работе я постоянно ощущаю психические и физические перегрузки
""",
"""
50. Успехи в работе вдохновляют меня
""",
"""
51. Ситуация на работе, в которой я оказался, кажется безвыходной (почти безвыходной)
""",
"""
52. Я потерял покой из-за работы
""",
"""
53. В течение последнего года бывали жалобы на меня со стороны партнёров
""",
"""
54. Мне удаётся сохранить нервы только благодаря тому, что многое из того, что происходит с моими партнёрами, я не принимаю близко к сердцу
""",
"""
55. Я часто приношу с работы домой отрицательные эмоции
""",
"""
56. Я часто работаю с трудом
""",
"""
57. Ранее я был более сочувствующим и внимательным к своим партнёрам, нежели теперь
""",
"""
58. В работе с людьми руководствуюсь принципом «не порти нервы, береги здоровье»
""",
"""
59. Иногда я иду на работу с тяжёлым чувством: как всё надоело, никого б не видеть и не слышать
""",
"""
60. После напряжённого рабочего дня я чувствую себя больным
""",
"""
61. Контингент партнёров, с которыми я работаю, очень трудный
""",
"""
62. Иногда мне кажется, что результаты моей работы не стоят тех усилий, которые я прикладываю
""",
"""
63. Если бы мне повезло с работой, я был бы намного счастливее
""",
"""
64. Я в отчаянии от того, что на работе у меня серьёзные проблемы
""",
"""
65. Иногда я веду себя с партнёрами так, как не хотел бы, чтобы они вели себя со мной
""",
"""
66. Я осуждаю партнёров, которые рассчитывают на особую снисходительность и внимание
""",
"""
67. Обычно после рабочего дня у меня не хватает сил заниматься домашними делами
""",
"""
68. Часто я подгоняю время: побыстрее бы закончился рабочий день
""",
"""
69. Состояние, просьбы, нужды партнёров обычно меня искренне волнуют
""",
"""
70. Работая с людьми, я обычно будто ставлю экран, защищающий меня от чужих страданий и отрицательных эмоций
""",
"""
71. Работа с людьми (с партнёрами) очень разочаровала меня
""",
"""
72. Чтобы восстановить силы, я часто принимаю лекарства
""",
"""
73. Как правило, мой рабочий день проходит спокойно и легко
""",
"""
74. Мои требования к выполняемой работе выше, нежели то, чего я достигаю в связи с некоторыми обстоятельствами
""",
"""
75. Моя карьера сложилась удачно
""",
"""
76. Я очень нервничаю по поводу того, что связано с работой
""",
"""
77. Некоторых из своих постоянных партнёров я не хотел бы видеть и слышать
""",
"""
78. Я одобряю коллег, которые полностью посвящают себя людям (партнёрам), пренебрегая собственными интересами
""",
"""
79. Моя усталость на работе обычно мало или вообще не отображается на общении с домочадцами и друзьями
""",
"""
80. По возможности я уделяю партнёру меньше внимания, но так, чтобы он этого не заметил
""",
"""
81. Меня часто подводят нервы в общении с людьми на работе
""",
"""
82. Ко всему (почти ко всему), что происходит на работе, я потерял заинтересованность, живое чувство
""",
"""
83. Работа с людьми плохо повлияла на меня как на специалиста – сделала нервным, злым, притупила эмоции
""",
"""
84. Работа с людьми, как оказалось, подрывает моё здоровье
""",
), 
    'uk': (
"""
1. Організаційні помилки на роботі постійно змушують мене нервувати, напружуватися, хвилюватися
""",
"""
2. Сьогодні я задоволений своєю професією не менше, ніж на початку кар’єри
""",
"""
3. Я помилився у виборі професії чи профілю діяльності (займаю не своє місце)
""",
"""
4. Мене турбує те, що я став гірше працювати (менш продуктивно, менш якісно, повільніше)
""",
"""
5. Теплота у взаємодії з партнерами дуже залежить від мого настрою
""",
"""
6. Від мене як від професіонала мало залежить добробут партнерів
""",
"""
7. Коли я приходжу з роботи додому, то деякий час (години 2-3) мені хочеться побути на самоті, щоб зі мною ніхто не спілкувався
""",
"""
8. Коли я відчуваю втому чи напруження, то намагаюся швидше вирішити проблеми партнера (згорнути взаємодію)
""",
"""
9. Мені здається, що емоційно я не можу дати колегам того, що вимагає професійний обов’язок
""",
"""
10. Моя робота притупляє емоції
""",
"""
11. Я відверто втомився від людських проблем, з якими доводиться мати справу по роботі
""",
"""
12. Трапляється, я погано засинаю (сплю) через хвилювання, які пов’язані з роботою
""",
"""
13. Взаємодія з партнерами потребує від мене великого напруження
""",
"""
14. Робота з людьми приносить мені все менше задоволення
""",
"""
15. Я б змінив місце роботи, якби з’явилась така можливість
""",
"""
16. Мене часто засмучує те, що я не можу на потрібному рівні надати професійну підтримку, послугу, допомогу
""",
"""
17. Мені завжди вдається запобігти впливу поганого настрою на ділові контакти
""",
"""
18. Мене дуже засмучує ситуація, коли щось не йде на лад у стосунках з діловими партнерами
""",
"""
19. Я так стомлююся на роботі, що вдома намагаюся спілкуватися якомога менше
""",
"""
20. Спілкування з партнерами спонукає мене уникати людей
""",
"""
21. Іноді звичні ситуації спілкування на роботі дратують мене
""",
"""
22. Я спокійно сприймаю обґрунтовані претензії партнерів
""",
"""
23. Спілкування з партнерами спонукає мене уникати людей
""",
"""
24. При згадці про деяких партнерів та колег у мене псується настрій
""",
"""
25. Конфлікти та суперечки з колегами забирають багато сил та емоцій
""",
"""
26. Мені все складніше встановлювати або підтримувати контакти з діловими партнерами
""",
"""
27. Обставини на роботі мені здаються дуже складними і важкими
""",
"""
28. У мене часто виникають тривожні очікування, пов’язані з роботою: щось має трапитися, як би не припуститися помилки, чи зможу зробити все, як потрібно, чи не скоротять мене тощо
""",
"""
29. Якщо партнер мені неприємний, то я намагаюся обмежити час спілкування з ним, менше приділяти йому уваги
""",
"""
30. У спілкуванні на роботі я дотримуюся принципу «не роби людям добра – не отримаєш зла»
""",
"""
31. Я з радістю розповідаю домашнім про свою роботу
""",
"""
32. Трапляються дні, коли мій емоційний стан погано відображається на результатах роботи (менше працюю, знижується якість, виникають конфлікти)
""",
"""
33. Іноді я відчуваю що потрібно поспівчувати партнерові, але я не в змозі цього зробити
""",
"""
34. Я дуже хвилююся за свою роботу
""",
"""
35. Партнерам по роботі віддаю я більше уваги та турботи, ніж отримую від них вдячності
""",
"""
36. При одній згадці про роботу мені стає погано: починає колоти в області серця, підвищується тиск, виникає головний біль
""",
"""
37. У мене добрі (в цілому задовільні) стосунки з безпосереднім керівництвом
""",
"""
38. Я часто радію, коли бачу, що моя робота приносить користь людям
""",
"""
39. Останнім часом мене переслідують невдачі на роботі
""",
"""
40. Деякі аспекти (факти) моєї роботи викликають розчарування, нудьгу і зневіру
""",
"""
41. Трапляються дні, коли контакти з партнерами складаються гірше, ніж зазвичай
""",
"""
42. Я переймаюся проблемами ділових партнерів (суб’єктів діяльності) менше, ніж зазвичай
""",
"""
43. Втома від роботи призводить до того, що я намагаюся скоротити час спілкування з друзями та знайомими
""",
"""
44. Зазвичай я виявляю зацікавленість особистістю партнера більше, ніж того вимагає справа
""",
"""
45. Зазвичай я приходжу на роботу відпочивши, із свіжими силами, в гарному настрої
""",
"""
46. Іноді я ловлю себе на тому, що працюю з партнерами автоматично, без душі
""",
"""
47. У справах зустрічаються настільки неприємні люди, що всупереч волі бажаєш їм чогось недоброго
""",
"""
48. Після спілкування з неприємними партнерами у мене буває погіршення фізичного та психічного самопочуття
""",
"""
49. На роботі я постійно відчуваю психічне та фізичне перевантаження
""",
"""
50. Успіхи в роботі надихають мене
""",
"""
51. Ситуація на роботі, в якій я опинився, здається безвихідною (майже безвихідною)
""",
"""
52. Я втратив спокій через роботу
""",
"""
53. Впродовж останнього року траплялися скарги на мене з боку партнерів
""",
"""
54. Мені вдається зберегти нерви тільки завдяки тому, що багато з того, що відбувається із моїми партнерами, я не беру близько до серця
""",
"""
55. Я часто з роботи приношу додому негативні емоції
""",
"""
56. Я часто працюю через силу
""",
"""
57. Раніше я був більш співчутливим та уважним до партнерів, ніж тепер
""",
"""
58. У роботі з людьми керуюся принципом «не псуй нерви, бережи здоров’я»
""",
"""
59. Іноді я йду на роботу з важким відчуттям: як все набридло, нікого б не бачити і не чути
""",
"""
60. Після напруженого робочого дня я відчуваю, що занедужав
""",
"""
61. Контингент партнерів, з якими я працюю, дуже важкий
""",
"""
62. Іноді мені здається, що результати моєї роботи не варті тих зусиль, які я витрачаю
""",
"""
63. Якщо б мені поталанило з роботою, я був би набагато щасливішим
""",
"""
64. Я у відчаї від того, що на роботі у мене серйозні проблеми
""",
"""
65. Іноді я поводжуся із своїми партнерами так, як би не хотів, щоб вони вчиняли зі мною
""",
"""
66. Я засуджую партнерів, що розраховують на особливу поблажливість та увагу
""",
"""
67. Зазвичай після робочого дня у мене не вистачає сил займатися домашніми справами
""",
"""
68. Часто я підганяю час: швидше б закінчився робочий день
""",
"""
69. Стан, прохання, потреби партнерів зазвичай мене щиро хвилюють
""",
"""
70. Працюючи з людьми, я зазвичай ніби ставлю екран, що захищає мене від чужих страждань та негативних емоцій
""",
"""
71. Робота з людьми (з партнерами) дуже розчарувала мене
""",
"""
72. Щоб відновити сили, я часто вживаю ліки
""",
"""
73. Як правило, мій робочий день проходить спокійно і легко
""",
"""
74. Мої вимоги до виконуваної роботи вищі, ніж те, чого я досягаю через певні обставини
""",
"""
75. Моя кар’єра склалася вдало
""",
"""
76. Я дуже нервую з приводу того, що пов’язано з роботою
""",
"""
77. Деяких із своїх постійних партнерів я не хотів би бачити і чути
""",
"""
78. Я схвалюю колег, які повністю присвячують себе людям (партнерам), нехтуючи власними інтересами
""",
"""
79. Моя втома на роботі зазвичай мало або взагалі не відображається на спілкуванні з домашніми і друзями
""",
"""
80. За можливістю, я приділяю партнерові менше уваги, але так, щоб він цього не помітив
""",
"""
81. Мене часто підводять нерви у спілкуванні з людьми на роботі
""",
"""
82. До всього (майже до всього), що відбувається на роботі, я втрати зацікавленість, живе почуття
""",
"""
83. Робота з людьми погано вплинула на мене як на фахівця – зробила знервованим, злим, притупила емоції
""",
"""
84. Робота з людьми, як виявилося, підриває моє здоров’я
""",
),
}

_ANSWERS = {
    'ru': [['Да', '%s.%s:1'], ['Нет', '%s.%s:-1']],
    'uk': [['Так', '%s.%s:1'], ['Ні', '%s.%s:-1']],
}

_no_ext_questions = ()

_EXT_ANSWERS = {
    'ru': [['Не знаю', '%s.%s:0']],
    'uk': [['Не знаю', '%s.%s:0']],
}

_PARAMS = {
    'ru': {
        '01' : 'Переживание психотравмирующих обстоятельств',
        '02' : 'Неудовлетворённость собой',
        '03' : '«Загнанность в угол»',
        '04' : 'Тревога и депрессия',
        '05' : 'Неадекватное избирательное эмоциональное реагирование',
        '06' : 'Эмоционально-моральная дезориентация',
        '07' : 'Расширение сферы экономии эмоций',
        '08' : 'Редукция профессиональных обязанностей',
        '09' : 'Эмоциональный дефицит',
        '10' : 'Эмоциональное отчуждение',
        '11' : 'Личностное отчуждение (деперсонализация)',
        '12' : 'Психосоматические и вегетативные нарушения',
    },
    'uk': {
        '01' : 'Переживання психотравмуючих обставин',
        '02' : 'Незадоволеність собою',
        '03' : '«Загнаність у кут»',
        '04' : 'Тривога і депресія',
        '05' : 'Неадекватне вибіркове емоційне реагування',
        '06' : 'Емоційно-моральна дезорієнтація',
        '07' : 'Розширення сфери економії емоцій',
        '08' : 'Редукція професійних обов’язків',
        '09' : 'Емоційний дефіцит',
        '10' : 'Емоційне відчуження',
        '11' : 'Особистісне відчуження (деперсоналізація)',
        '12' : 'Психосоматичні та психовегетативні порушення',
    },
}

_SCORES = {
    'ru': {
        '01' : [{1:2, 13:3, 25:2, 49:10, 61:5}, {37:3, 73:5}],
        '02' : [{14:2, 26:2, 62:5, 74:3}, {2:3, 38:10, 50:5}],
        '03' : [{3:10, 15:5, 27:2, 39:2, 51:5, 63:1}, {75:5}],
        '04' : [{4:2, 16:3, 28:5, 40:5, 52:10, 54:2, 76:3}, {}],
        '05' : [{5:5, 29:10, 41:2, 53:2, 65:3, 77:5}, {17:3}],
        '06' : [{6:10, 30:3, 42:5, 54:2, 66:2}, {18:3, 75:5}],
        '07' : [{7:2, 19:10, 43:5, 55:3, 67:3}, {31:2, 79:5}],
        '08' : [{8:5, 20:5, 32:2, 56:3, 68:3, 80:10}, {44:2}],
        '09' : [{9:3, 21:2, 33:5, 57:3, 81:2}, {45:5, 69:10}],
        '10' : [{10:2, 22:3, 46:3, 58:5, 70:5, 82:10}, {34:2}],
        '11' : [{11:5, 23:3, 35:3, 47:2, 59:5, 71:2, 83:10}, {}],
        '12' : [{12:3, 24:2, 36:5, 48:3, 60:2, 72:10, 84:5}, {}],
    },
    'uk': {
        '01' : [{1:2, 13:3, 25:2, 49:10, 61:5}, {37:3, 73:5}],
        '02' : [{14:2, 26:2, 62:5, 74:3}, {2:3, 38:10, 50:5}],
        '03' : [{3:10, 15:5, 27:2, 39:2, 51:5, 63:1}, {75:5}],
        '04' : [{4:2, 16:3, 28:5, 40:5, 52:10, 54:2, 76:3}, {}],
        '05' : [{5:5, 29:10, 41:2, 53:2, 65:3, 77:5}, {17:3}],
        '06' : [{6:10, 30:3, 42:5, 54:2, 66:2}, {18:3, 75:5}],
        '07' : [{7:2, 19:10, 43:5, 55:3, 67:3}, {31:2, 79:5}],
        '08' : [{8:5, 20:5, 32:2, 56:3, 68:3, 80:10}, {44:2}],
        '09' : [{9:3, 21:2, 33:5, 57:3, 81:2}, {45:5, 69:10}],
        '10' : [{10:2, 22:3, 46:3, 58:5, 70:5, 82:10}, {34:2}],
        '11' : [{11:5, 23:3, 35:3, 47:2, 59:5, 71:2, 83:10}, {}],
        '12' : [{12:3, 24:2, 36:5, 48:3, 60:2, 72:10, 84:5}, {}],
    },
}

_RESULTS = {
    'ru' : (
        ( 9, 'Симптом не сформирован'), 
        (15, 'Симптом на стадии формирования'), 
        (30, 'Симптом сформирован'), 
    ),
    'uk' : (
        ( 9, 'Симптом не сформований'), 
        (15, 'Симптом на стадії формування'), 
        (30, 'Симптом сформований'), 
    ),
}

_MODE_CONTROL = ()

_CONCLUSIONS = {
    'ru' : {
        'F1' : ('= Фаза напряжённости', ('01','02','03','04'), [(36, 'Фаза не сформирована'), (60, 'Фаза на стадии формирования'), (120, 'Фаза сформирована')]),
        'F2' : ('= Фаза резистенции', ('05','06','07','08'), [(36, 'Фаза не сформирована'), (60, 'Фаза на стадии формирования'), (120, 'Фаза сформирована')]),
        'F3' : ('= Фаза истощения', ('09','10','11','12'), [(36, 'Фаза не сформирована'), (60, 'Фаза на стадии формирования'), (120, 'Фаза сформирована')]),
    },
    'uk' : {
        'F1' : ('= Фаза напруженості', ('01','02','03','04'), [(36, 'Фаза не сформована'), (60, 'Фаза на стадії формування'), (120, 'Фаза сформирована')]),
        'F2' : ('= Фаза резистенції', ('05','06','07','08'), [(36, 'Фаза не сформована'), (60, 'Фаза на стадії формування'), (120, 'Фаза сформирована')]),
        'F3' : ('= Фаза виснаження', ('09','10','11','12'), [(36, 'Фаза не сформована'), (60, 'Фаза на стадії формування'), (120, 'Фаза сформирована')]),
    },
}

_HEADERS = {
    'ru': 
"""
На каждое из предложенных ниже утверждений дайте ответ «да» или «нет». Обратите внимание: если в формулировках вопросов упоминаются партнёры, то речь идёт о субъектах вашей профессиональной деятельности – пациентах, клиентах, учеников, студентов, работников и других лиц, с которыми вы каждый день работаете.
""",
    'uk': 
"""
На кожне із запропонованих нижче тверджень дайте відповідь «так» чи «ні». Візьміть до уваги: якщо у формулюваннях запитань згадуються партнери, то мова йдеться про суб’єктів вашої професійної діяльності – пацієнтів, клієнтів, учнів, студентів, працівників та інших осіб, з якими ви щоденно працюєте.
""",
}

_WARNINGS = {
    'ru': (
"""
Внимание, предоставленные данные выглядят недостоверными, рекомендуется быть более искренним в ответах или обратиться к специалисту!
""",
), 
    'uk': (
"""
Увага, надані відповіді видаються не надто достовірними; рекомендується бути більш щирим у відповідях або звернутися до фахівця!
""",
),
}

_FINISH = {
    'ru': (
"""
Завершение диалога.
""",
"""
Мы благодарим Вас за Ваши ответы.
Желаем Вам крепкого здоровья, и всего Вам доброго!
""",
), 
    'uk': (
"""
Завершення діалогу.
""",
"""
Ми дякуємо Вам за Ваші відповіді.
Бажаємо Вам міцного здоров'я, і всього Вам доброго!
""",
),
}

_results = {}


def test_name():
    return _TEST_NAME

def total_questions():
    return _QCOUNT

def get_question(i, lang, no_eof=None):
    x = _QUESTIONS[lang][i].strip()
    s = '%s.%s.' % (_TEST_NAME, x[-1] == '.' and x[:-1] or x)
    return no_eof and re.sub(r'\n', ' ', s) or s

def get_header(lang, no_eof=None):
    s = '<b>%s</b>' % _HEADERS[lang].strip()
    return no_eof and re.sub(r'\n', ' ', s) or s

def get_finish(storage, name, i, lang, no_eof=None):
    nic = storage.get(name, 'nic', with_decode=True)
    s = '%s%s' % (nic and '%s!\n\n' % nic or _FINISH[lang][0], _FINISH[lang][i].strip())
    return no_eof and re.sub(r'\n', ' ', s) or s

def get_result(storage, name, lang):
    global _results

    res = ''

    data = storage.getall(name)
    params = _PARAMS[lang]
    scores = _SCORES[lang]
    results = _RESULTS[lang]
    conclusions = _CONCLUSIONS[lang]

    keys = sorted([x for x in params.keys() if x.isdigit()])

    cs, px = {}, {}

    for p in keys:
        # p: ключ параметра: 01,02...
        # name: наименование параметра
        x = 0
        name = params[p]
        for i in range(0, 2):
            # i=0: группа "Да"
            # i=1: группа "Нет"
            # sc: словарь ответов по каждой группе
            sc = scores[p][i]
            for n in sc.keys():
                # n: номер вопроса
                # score: баллы за ответ на вопрос
                score = sc[n]*(i == 0 and 1 or -1)
                key = ('%s.%s' % (_TEST_NAME, n)).encode()
                v = int(data.get(key, 0))
                if i == 0 and v < 0:
                    continue
                if i == 1 and v > 0:
                    continue
                x += v*score

        px[p] = x

        c = ''
        for i, item in enumerate(results):
            # i: индекс результата
            # item: граничное значение параметра
            if x <= item[0]:
                # c: итоговая оценка по параметру
                c = item[1]
                if _with_group:
                    if i not in cs:
                        cs[i] = []
                    cs[i].append(p)
                break

        _results[p] = (x, c)

        # res: текст результата (симптомы)
        if not _with_group:
            res += '%s. %s: [%s] <b>%s</b>\n' % (p, name, x, c)

    if _with_group:
        for i in cs:
            res += '<b>%s:</b>\n' % results[i][1]
            for p in cs[i]:
                res += '    %s: [%s] %s\n' % (p, px[p], params[p])

    res += ' * '*3+'\n'

    for k in conclusions:
        # k: ключ параметра: F1,F2,F3
        c, x = '', 0
        # name: наименование параметра
        # group: группа параметров
        # conclusion: характеристика (группа ответов)
        name, group, conclusion = conclusions[k]
        for p in group:
            if p not in _results:
                continue
            x += _results[p][0]
            for i, item in enumerate(conclusion):
                # item: граничное значение параметра
                if x <= item[0]:
                    # c: итоговая оценка по параметру
                    c = item[1]
                    break

        _results[k] = (x, c)

        # res: текст результата (фазы)
        res += '%s. %s: [%s] <b>%s</b>\n' % (k, name, x, c)

    return res.strip()

def answer(bot, message, command, data=None, logger=None, question=None, **kw):
    """
        Make the step's answer
        
        Коды результатов:
        
            =P - параметр (наименование, текст)
        
            RP - результат по параметру (число)
            TP - диагноз по параметру (текст)
            RC - итоговый результат (число)
            TC - итоговый диагноз (текст)
    """
    lang = kw.get('lang') or DEFAULT_LANGUAGE
    storage = kw.get('storage')
    name = kw.get('name')

    is_run = True

    if question == 0:
        text = get_header(lang)
        bot.send_message(message.chat.id, text, parse_mode=DEFAULT_PARSE_MODE)

    if question == _QCOUNT or (IsDebug and question > 0 and question%10 == 0):
        result = get_result(storage, name, lang)
        bot.send_message(message.chat.id, result, parse_mode=DEFAULT_PARSE_MODE)
        is_run = question < _QCOUNT

        if is_run:
            time.sleep(3)

    if is_run:
        answers = deepcopy(_ANSWERS[lang])
        if _with_extra:
            if question not in _no_ext_questions:
                answers += deepcopy(_EXT_ANSWERS[lang])
        for i, a in enumerate(answers):
            answers[i][1] = answers[i][1] % (_TEST_NAME, question+1)
        send_inline_keyboard(bot, message, answers, get_question(question, lang))

    elif 'query_id' in kw:
        _test_name = test_name()

        dbs.drop_before(_test_name, **kw)
        dbs.save_params(_test_name, _PARAMS, _results, is_not_tuple=1, **kw)

        if not _is_without_conclusions:
            dbs.save_conclusions(_test_name, _CONCLUSIONS, _results, **kw)  #XXX conclusions!
        """
        for p in sorted([x for x in _PARAMS[lang].keys()]):
            if p in _results:
                param = _PARAMS[lang][p]
                value, s1 = _results[p]
                storage.set(name, '%s.RP%s' % (_TEST_NAME, p), value)
                storage.set(name, '%s.TP%s' % (_TEST_NAME, p), '<i>%s</i>. %s:%s' % (param, s1, value), with_encode=True)
                storage.set(name, '%s.=P%s' % (_TEST_NAME, p), param, with_encode=True)

        if not _is_without_conclusions:
            conclusions = _CONCLUSIONS[lang]
            for p in sorted(list(conclusions.keys())):
                if p in _results:
                    param = conclusions[p][0]
                    value, s1 = _results[p]
                    storage.set(name, '%s.RC%s' % (_TEST_NAME, p), value)
                    storage.set(name, '%s.TC%s' % (_TEST_NAME, p), v2:='<i>%s</i>. %s:%s' % (param, s1, value), with_encode=True)
        """
        if kw['query_id']:
            bot.answer_callback_query(
                kw['query_id'],
                text=get_finish(storage, name, 1, lang),
                show_alert=True
                )

            time.sleep(3)

        help(bot, message, logger=logger, mode=1, **kw)

## -------------------------- ##

def lines(text):
    for line in text.split('\n'):
        if not line:
            continue
        x = line.split('.')
        n, s = int(x[0].strip()), x[1].strip()
        print('"""\n%s. %s\n""",' % (n, s))

def check(data, key, param, lang='ru'):
    scores = _SCORES[lang]
    res = scores[param]
    s = 0
    for k in data[key].keys():
        #print(k)
        q = k.split('.')[1]
        if not q.isdigit():
            continue
        q = int(q)
        #print(q)
        v = int(data[key][k])
        for i in range(0, 2):
            if q in res[i].keys():
                if i == 0 and v < 0:
                    continue
                if i == 1 and v > 0:
                    continue
                r = int(res[i][q])
                s += r*v*(i == 0 and 1 or -1)
    return s

def selftest(data, lang, with_print=None):
    key = _TEST_NAME
    params = _PARAMS[lang]
    conclusions = _CONCLUSIONS[lang]

    out = []
    r = {}
    for i, p in enumerate(sorted(params.keys())):
        x = check(data, key, p, lang=lang)
        if with_print:
            print(x)

        rp = '%s.RP%s' % (key, p)
        if rp in data[key]:
            r[rp] = int(data[key].get(rp, '0'))
            out.append(r[rp] == x and 'OK.%s [%s]' % (p, x) or 'Error %s [%s:%s]' % (rp, x, r[rp]))
            if with_print:
                print(out[i])
        else:
            out.append(NO_RESULTS)

    for p in conclusions.keys():
        name, keys, values = conclusions[p]
        x = sum([r.get('%s.RP%s' % (key, k), 0) for k in keys])
        rc = '%s.RC%s' % (key, p)
        if rc in data[key]:
            c = int(data[key].get(rc, '0'))
            out.append(c == x and 'OK.%s [%s]' % (p, x) or 'Error %s [%s:%s]' % (rc, x, c))
            if with_print:
                print(out[i])
        else:
            out.append(NO_RESULTS)

    is_ok, is_error = 1, 0
    for s in out:
        if s.startswith('OK'):
            pass
        elif s.startswith('Error'):
            is_ok = 0
            is_error = 1
            if with_print or IsWithPrintErrors:
                print(key, s)
            break
        else:
            is_ok = 0
            break

    return is_ok and 'OK' or is_error and 'Error' or NO_RESULTS
