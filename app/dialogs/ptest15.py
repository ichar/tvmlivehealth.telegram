# -*- coding: utf-8 -*-

import re
import time
from copy import deepcopy
import random

from config import (
     IsDebug, IsDeepDebug, IsTrace, IsPrintExceptions, IsWithPrintErrors, IsWithGroup, IsWithExtra,
     errorlog, print_to, print_exception,
    )

from app.settings import DEFAULT_LANGUAGE, DEFAULT_PARSE_MODE, NO_RESULTS, NO_KEY, RCODES
from app.dialogs.start import help
from app.handlers import *

from app import dbs

# Группировка результатов
_with_group = IsWithGroup
# Ответ "Не знаю"
_with_extra = IsWithExtra

# Финальный результат теста
_is_without_conclusions = 1

# -------------------------------------
# Тест на акцентуацию характера Шмишека
# -------------------------------------

_TEST_NAME = 'T15'
_QCOUNT = 88
_QCOUNT_EXT = 61

_QUESTIONS = {
    'ru': (
"""
1. Является ли ваше настроение в общем весёлым и беззаботным?
""",
"""
2. Восприимчивы ли вы к обидам?
""",
"""
3. Случалось ли вам иногда быстро заплакать?
""",
"""
4. Всегда ли вы считаете себя правым в том деле, которое делаете, и вы не успокоитесь, пока не убедитесь в этом?
""",
"""
5. Считаете ли вы себя более смелым, чем в детском возрасте?
""",
"""
6. Может ли ваше настроение меняться от глубокой радости до глубокой печали?
""",
"""
7. Находитесь ли вы в компании в центре внимания?
""",
"""
8. Бывают ли у вас дни, когда вы без достаточных оснований находитесь в угрюмом и раздражительном настроении и ни с кем не хотите разговаривать?
""",
"""
9. Серьёзный ли вы человек?
""",
"""
10. Можете ли вы сильно воодушевиться?
""",
"""
11. Предприимчивы ли вы?
""",
"""
12. Быстро ли вы забываете, когда вас кто-нибудь обидит?
""",
"""
13. Мягкосердечный ли вы человек?
""",
"""
14. Пытаетесь ли вы проверить после того, как опустили письмо в почтовый ящик, не осталось ли оно висеть в прорези?
""",
"""
15. Всегда ли вы стараетесь быть добросовестным в работе?
""",
"""
16. Испытывали ли вы в детстве страх перед грозой или собаками?
""",
"""
17. Считаете ли вы других людей недостаточно требовательными друг к другу?
""",
"""
18. Сильно ли зависит ваше настроение от жизненных событий и переживаний?
""",
"""
19. Всегда ли вы прямодушны со своими знакомыми?
""",
"""
20. Часто ли ваше настроение бывает подавленным?
""",
"""
21. Был ли у вас раньше истерический припадок или истощение нервной системы?
""",
"""
22. Склонны ли вы к состояниям сильного внутреннего беспокойства или страстного стремления?
""",
"""
23. Трудно ли вам длительное время просидеть на стуле?
""",
"""
24. Боретесь ли вы за свои интересы, если кто-то поступает с вами несправедливо?
""",
"""
25. Смогли бы вы убить человека?
""",
"""
26. Настолько ли сильно вам мешает косо висящая гардина или неровно постеленная скатерть, что вам хочется немедленно устранить эти недостатки?
""",
"""
27. Испытывали ли вы в детстве страх, когда оставались одни в квартире?
""",
"""
28. Часто ли у вас без причины меняется настроение?
""",
"""
29. Всегда ли вы старательно относитесь к своей деятельности?
""",
"""
30. Быстро ли вы можете разгневаться?
""",
"""
31. Можете ли вы быть бесшабашно весёлым?
""",
"""
32. Можете ли вы иногда целиком проникнуться чувством радости?
""",
"""
33. Подходите ли вы для проведения увеселительных мероприятий?
""",
"""
34. Высказываете ли вы обычно людям своё откровенное мнение по тому или иному вопросу?
""",
"""
35. Влияет ли на вас вид крови?
""",
"""
36. Охотно ли вы занимаетесь деятельностью, связанной с большой ответственностью?
""",
"""
37. Склонны ли вы вступиться за человека, с которым поступили несправедливо?
""",
"""
38. Трудно ли вам входить в тёмный подвал?
""",
"""
39. Выполняете ли вы кропотливую чёрную работу так же медленно и тщательно, как и любимое ваше дело?
""",
"""
40. Являетесь ли вы общительным человеком?
""",
"""
41. Охотно ли вы декламировали в школе стихи?
""",
"""
42. Убегали ли вы ребёнком из дома?
""",
"""
43. Тяжело ли вы воспринимаете жизнь?
""",
"""
44. Бывали ли у вас конфликты и неприятности, которые так изматывали вам нервы, что вы не выходили на работу?
""",
"""
45. Можно ли сказать, что вы при неудачах не теряете чувство юмора?
""",
"""
46. Сделаете ли вы первым шаг к примирению, если вас кто-то оскорбит?
""",
"""
47. Любите ли вы животных?
""",
"""
48. Уйдёте ли вы с работы или из дому, если у вас там что-то не в порядке?
""",
"""
49. Мучают ли вас неопределённые мысли, что с вами или с вашими родственниками случится какое-нибудь несчастье?
""",
"""
50. Считаете ли вы, что настроение зависит от погоды?
""",
"""
51. Затруднит ли вас выступить на сцене перед большим количеством зрителей?
""",
"""
52. Можете ли вы выйти из себя и дать волю рукам, если вас кто-то умышленно грубо рассердит?
""",
"""
53. Много ли вы общаетесь?
""",
"""
54. Если вы будете чем-либо разочарованы, придёте ли в отчаяние?
""",
"""
55. Нравится ли вам работа организаторского характера?
""",
"""
56. Упорно ли вы стремитесь к своей цели, даже если на пути встречается много препятствий?
""",
"""
57. Может ли вас так захватить кинофильм, что слёзы выступят на глазах?
""",
"""
58. Трудно ли вам будет заснуть, если вы целый день размышляли над своим будущим или какой-нибудь проблемой?
""",
"""
59. Приходилось ли вам в школьные годы пользоваться подсказками или списывать у своих товарищей домашнее задание?
""",
"""
60. Трудно ли вам пойти ночью на кладбище?
""",
"""
61. Следите ли вы с большим вниманием, чтобы каждая вещь в доме лежала на своём месте?
""",
"""
62. Приходилось ли вам лечь спать в хорошем настроении, а проснуться в удручённом и несколько часов оставаться в нём?
""",
"""
63. Можете ли вы с лёгкостью приспособиться к новой ситуации?
""",
"""
64. Есть ли у вас предрасположенность к головной боли?
""",
"""
65. Часто ли вы смеётесь?
""",
"""
66. Можете ли вы быть приветливыми с людьми, не открывая своего истинного отношения к ним?
""",
"""
67. Можно ли вас назвать оживлённым и бойким человеком?
""",
"""
68. Сильно ли вы страдаете из-за несправедливости?
""",
"""
69. Можно ли вас назвать страстным любителем природы?
""",
"""
70. Есть ли у вас привычка проверять перед сном или перед тем, как уйти, выключены ли газ и свет, закрыта ли дверь?
""",
"""
71. Пугливы ли вы?
""",
"""
72. Бывает ли, что вы чувствуете себя на седьмом небе, хотя объективных причин для этого нет?
""",
"""
73. Охотно ли вы участвовали в юности в кружке художественной самодеятельности, в театральном кружке?
""",
"""
74. Тянет ли вас иногда смотреть вдаль?
""",
"""
75. Смотрите ли вы на будущее пессимистически?
""",
"""
76. Может ли ваше настроение измениться от высочайшей радости до глубокой тоски за короткий период времени?
""",
"""
77. Легко ли поднимается ваше настроение в дружеской компании?
""",
"""
78. Чувствуете ли вы злость длительное время?
""",
"""
79. Сильно ли вы переживаете, если горе случилось у другого человека?
""",
"""
80. Была ли у вас в школе привычка переписывать лист в тетради, если вы поставили на него кляксу?
""",
"""
81. Можно ли сказать, что вы больше недоверчивы и осторожны, нежели доверчивы?
""",
"""
82. Часто ли вы видите страшные сны?
""",
"""
83. Возникала ли у вас мысль против воли броситься из окна, под приближающийся поезд?
""",
"""
84. Становитесь ли вы радостным в весёлом окружении?
""",
"""
85. Легко ли вы можете отвлечься от обременительных вопросов и не думать о них?
""",
"""
86. Трудно ли вам сдержать себя, если вы разозлитесь?
""",
"""
87. Предпочитаете ли вы молчать (ответ «да»), или вы словоохотливы (ответ «нет»)?
""",
"""
88. Могли бы вы, если пришлось бы участвовать в театральном представлении, с полным проникновением и перевоплощением войти в роль и забыть о себе?
""",
), 
    'uk': (
"""
1. Чи є ваш настрій загалом веселим і безтурботним?
""",
"""
2. Ви чутливі до образ?
""",
"""
3. Чи траплялося вам іноді швидко заплакати?
""",
"""
4. Ви завжди ви вважаєте, що маєте рацію у виконуваній роботі, і ви не заспокоїтеся, доки не переконаєтеся у цьому?
""",
"""
5. Вважаєте ви себе сміливішим, ніж були у дитячому віці?
""",
"""
6. Може ваш настрій змінюватися від глибокої радості до глибокого суму?
""",
"""
7. Ви знаходитися у товаристві в центрі уваги?
""",
"""
8. Бувають у вас дні, коли ви без достатніх причин знаходитеся в похмурому і роздратованому настрої й ні з ким не хочете розмовляти?
""",
"""
9. Ви серйозна людина?
""",
"""
10. Ви можете перебувати у піднесеному стані?
""",
"""
11. Ви підприємливі?
""",
"""
12. Ви швидко забуваєте, коли вас хто-небудь образить?
""",
"""
13. Ви м’якосерда людина?
""",
"""
14. Чи намагаєтеся ви, опустивши лист у поштову скриньку, перевірити, чи не залишилося воно висіти у щілині?
""",
"""
15. Ви завжди намагаєтеся бути ретельним у роботі?
""",
"""
16. Чи відчували ви у дитинстві страх перед грозою або собаками?
""",
"""
17. Чи вважаєте ви інших людей недостатньо вимогливими один до одного?
""",
"""
18. Ваш настрій сильно залежить від життєвих подій та переживань?
""",
"""
19. Ви завжди щирі зі своїми знайомими?
""",
"""
20. Ваш настрій часто буває пригніченим?
""",
"""
21. У вас був раніше істеричний напад чи виснаження нервової системи?
""",
"""
22. Чи схильні ви до станів сильного внутрішнього занепокоєння чи пристрасного намагання?
""",
"""
23. Вам важко тривалий час всидіти на стільці?
""",
"""
24. Чи боретеся ви за свої інтереси, якщо хтось вчиняє з вами несправедливо?
""",
"""
25. Ви змогли би вбити людину?
""",
"""
26. Чи настільки сильно вам заважає гардина, що косо висить, чи нерівно застелена скатертина, що вам хочеться негайно усунути ці недоліки?
""",
"""
27. Ви відчували ви у дитинстві страх, коли залишалися вдома на самоті?
""",
"""
28. Чи часто у вас без причини змінюється настрій?
""",
"""
29. Ви завжди ретельно ставитеся до своєї діяльності?
""",
"""
30. Ви швидко можете розгніватися?
""",
"""
31. Чи можете ви бути відчайдушно веселим?
""",
"""
32. Ви можете іноді повністю перейнятися відчуттям радості?
""",
"""
33. Ви підходите для проведення розважальних заходів?
""",
"""
34. Ви зазвичай висловлюєте людям свою відверту думку з того чи іншого питання?
""",
"""
35. На вас впливає вигляд крові?
""",
"""
36. Чи охоче ви займаєтеся діяльністю, пов’язаною з великою відповідальністю?
""",
"""
37. Чи схильні ви заступитися за людину, щодо якої вчинили несправедливо?
""",
"""
38. Вам важко заходити у темний підвал?
""",
"""
39. Ви виконуєте копітку чорну роботу так само повільно і ретельно, як і вашу улюблену справу?
""",
"""
40. Ви є товариською людиною?
""",
"""
41. Ви охоче декламували вірші у школі?
""",
"""
42. Ви, будучи дитиною, тікали з дому?
""",
"""
43. Ви важко сприймаєте життя?
""",
"""
44. Чи бували у вас конфлікти і неприємності, які так виснажували вам нерви, що ви не виходили на роботу?
""",
"""
45. Чи можна сказати, що при невдачах ви не втрачаєте почуття гумору?
""",
"""
46. Ви зробите перший крок до примирення, якщо вас хтось образить?
""",
"""
47. Ви любите тварин?
""",
"""
48. Ви підете з роботи чи з дому, якщо у вас там щось не до ладу?
""",
"""
49. Вас турбують невизначені думки, що з вами чи вашими родичами трапиться якесь нещастя?
""",
"""
50. Чи вважаєте ви, що настрій залежить від погоди?
""",
"""
51. Вас обтяжить виступити на сцені перед великою кількістю глядачів?
""",
"""
52. Чи можете ви вийти із себе і дати волю рукам, якщо хтось вас навмисно грубо розсердить?
""",
"""
53. Ви багато спілкуєтеся?
""",
"""
54. Якщо ви будете чимось розчаровані, то прийдете у відчай?
""",
"""
55. Вам подобається робота організаторського характеру?
""",
"""
56. Ви наполегливо прагнете досягти мети, навіть якщо на шляху зустрічається багато перешкод?
""",
"""
57. Вас може так захопити кінофільм, що на очах виступлять сльози?
""",
"""
58. Вам важко буде заснути, якщо ви цілий день розмірковували над своїм майбутнім чи якою-небудь проблемою?
""",
"""
59. Вам доводилося у шкільні роки користуватися підказками чи списувати у своїх товаришів домашнє завдання?
""",
"""
60. Вам важко піти вночі на цвинтар?
""",
"""
61. Чи стежите ви з великою уважністю, аби кожна річ вдома лежала на своєму місці?
""",
"""
62. Вам доводилося лягти спати у доброму настрої, а прокинутися в пригніченому і кілька годин залишатися в ньому?
""",
"""
63. Ви можете легко пристосуватися до нової ситуації?
""",
"""
64. У вас є схильність до головного болю?
""",
"""
65. Ви часто смієтеся?
""",
"""
66. Ви можете бути привітними з людьми, не показуючи їм свого істинного ставлення до них?
""",
"""
67. Вас можна назвати жвавою і моторною людиною?
""",
"""
68. Ви сильно страждаєте від несправедливості?
""",
"""
69. Вас можна назвати пристрасним любителем природи?
""",
"""
70. У вас є звичка перевіряти перед сном чи перед тим, як піти, чи вимкнені газ та світло, чи зачинені двері?
""",
"""
71. Ви лякливі?
""",
"""
72. Чи буває, що ви почуваєтеся на сьомому небі, хоча об’єктивних причин для цього немає?
""",
"""
73. В юності ви охоче брали участь у гуртку художньої самодіяльності, у театральному гуртку?
""",
"""
74. Вас іноді тягне подивитися вдалечінь?
""",
"""
75. Ви песимістично дивитеся на майбутнє?
""",
"""
76. Чи може ваш настрій змінитися від найглибшої радості до глибокого суму за короткий проміжок часу?
""",
"""
77. Ваш настрій легко підіймається у дружньому товаристві?
""",
"""
78. Ви відчуваєте гнів протягом довгого часу?
""",
"""
79. Ви сильно переживаєте, якщо горе трапилося у іншої людини?
""",
"""
80. У вас була в школі звичка переписувати аркуш в зошиті, якщо ви його заляпали?
""",
"""
81. Чи можна сказати, що ви швидше недовірливі і обережні, аніж довірливі?
""",
"""
82. Ви часто бачите нічні жахіття?
""",
"""
83. Чи виникала у вас думка всупереч волі кинутися з вікна, під потяг, що наближається?
""",
"""
84. Ви стаєте радісним у веселому оточенні?
""",
"""
85. Чи легко ви можете відволіктися від обтяжливих питань і не думати про них?
""",
"""
86. Вам важко втриматися, коли ви розгнівані?
""",
"""
87. Ви надаєте перевагу мовчати (відповідь «так»), чи ви говіркі (відповідь «ні»)?
""",
"""
88. Чи могли б ви, якби довелося брати участь у театральній виставі, з повним зануренням і перевтіленням увійти в роль і забути про себе?
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
        '01' : ('Гипертимность',      3, ([1, 11, 23, 33, 45, 55, 67, 77], [])),
        '02' : ('Эмоциональность',    3, ([3, 13, 35, 47, 57, 69, 79], [25])),
        '03' : ('Тревожность',        3, ([16, 27, 38, 49, 60, 71, 82], [5])),
        '04' : ('Демонстративность',  2, ([7, 19, 22, 29, 41, 44, 63, 66, 73, 85, 88], [51])),
        '05' : ('Дистимичность',      3, ([9, 21, 43, 75, 87], [31, 53, 65])),
        '06' : ('Застревание',        2, ([2, 15, 24, 34, 37, 56, 68, 78, 81], [12, 46, 59])),
        '07' : ('Педантичность',      2, ([4, 14, 17, 26, 39, 48, 58, 61, 70, 80, 83], [36])),
        '08' : ('Циклотимность',      3, ([6, 18, 28, 40, 50, 62, 72, 84], [])),
        '09' : ('Возбудимость',       3, ([8, 20, 30, 42, 52, 64, 74, 86], [])),
        '10' : ('Экзальтированность', 6, ([10, 32, 54, 76], [])),
    },
    'uk': {
        '01' : ('Гіпертимність',      3, ([1, 11, 23, 33, 45, 55, 67, 77], [])),
        '02' : ('Емоційність',        3, ([3, 13, 35, 47, 57, 69, 79], [25])),
        '03' : ('Тривожність',        3, ([16, 27, 38, 49, 60, 71, 82], [5])),
        '04' : ('Демонстративність',  2, ([7, 19, 22, 29, 41, 44, 63, 66, 73, 85, 88], [51])),
        '05' : ('Дистимічність',      3, ([9, 21, 43, 75, 87], [31, 53, 65])),
        '06' : ('Застрягання',        2, ([2, 15, 24, 34, 37, 56, 68, 78, 81], [12, 46, 59])),
        '07' : ('Педантичність',      2, ([4, 14, 17, 26, 39, 48, 58, 61, 70, 80, 83], [36])),
        '08' : ('Циклотимність',      3, ([6, 18, 28, 40, 50, 62, 72, 84], [])),
        '09' : ('Збудливість',        3, ([8, 20, 30, 42, 52, 64, 74, 86], [])),
        '10' : ('Екзальтованість',    6, ([10, 32, 54, 76], [])),
    },
}

_RESULTS = {
    'ru' : (
        (12, 'Свойство не выражено'), 
        (18, 'Средняя степень выраженности свойства'), 
        (24, 'Свойство выражено (акцентуировано)'), 
    ),
    'uk' : (
        (12, 'Властивість не виражена'), 
        (18, 'Середній ступінь вираженості властивості'), 
        (24, 'Властивість виражена (акцентуйована)'), 
    ),
}

_CONCLUSIONS = {
    'ru' : {
        'F1' : ([(0, ''), (0, ''), (0, '')]),
    },
    'uk' : {
        'F1' : ([(0, ''), (0, ''), (0, '')]),
    },
}

_HEADERS = {
    'ru': 
"""
Вам предлагается ряд вопросов. На каждый из них ответьте «да», если вы с ним согласны, и «нет», если для вас это нехарактерно.
""",
    'uk': 
"""
Вам пропонується низка запитань. На кожне з них дайте відповідь «так», якщо ви з ним згодні, чи «ні», якщо для вас це нехарактерно.
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
    s = '%s.%s' % (_TEST_NAME, x[-1] == '.' and x[:-1] or x)
    return no_eof and re.sub(r'\n', ' ', s) or s

def get_finish(storage, name, i, lang, no_eof=None):
    nic = storage.get(name, 'nic', with_decode=True)
    s = '%s%s' % (nic and '%s!\n\n' % nic or _FINISH[lang][0], _FINISH[lang][i].strip())
    return no_eof and re.sub(r'\n', ' ', s) or s

def get_result(storage, name, lang, mode=None):
    global _results

    res = ''

    data = storage.getall(name)
    params = _PARAMS[lang]
    results = _RESULTS[lang]
    conclusions = _CONCLUSIONS[lang]

    if mode == 1:
        keys = sorted([x for x in params.keys() if x[0].isdigit()])
    else:
        keys = sorted([x for x in params.keys() if x[0] in 'LF'])

    cs, px = {}, {}

    for p in keys:
        # p: ключ параметра: LF или 1...8
        x = 0
        for i in range(0, 2):
            # i=0: группа "Да"
            # i=1: группа "Нет"
            # score: баллы за ответ на вопрос
            score = 1
            for n in params[p][2][i]:
                # n: номер вопроса
                key = ('%s.%s' % (_TEST_NAME, n)).encode()
                v = int(data.get(key, 0))
                x += i == 0 and v > 0 and score or i == 1 and v < 0 and score or 0

        # param: наименование параметра
        param = params[p][0]
        # m: множитель параметра
        x = x * params[p][1]

        _results[p] = [x, '...']

        if mode == 1:
            px[p] = x
            c = ''
            for i, item in enumerate(results):
                # item: граничное значение параметра
                if x <= item[0]:
                    # c: итоговая оценка по параметру
                    c = item[1]
                    _results[p][1] = c
                    if _with_group:
                        if i not in cs:
                            cs[i] = []
                        cs[i].append(p)
                    break
            # res: текст результата
            if not _with_group:
                res += '%s. %s: [%s] <b>%s</b>\n' % (p, param, x, c)
        else:
            if x > 5:
                return True

    if mode == 1:
        if _with_group:
            for i in cs:
                res += '<b>%s:</b>\n' % results[i][1]
                for p in cs[i]:
                    res += '    %s. %s: [%s]\n' % (p, params[p][0], px[p])

    res += ' * '*3+'\n'

    if not _is_without_conclusions:
        x = sum([_results[p][0] for p in keys])
    
        for conclusion in conclusions.keys():
            c = ''
            for i, item in enumerate(conclusion):
                # item: граничное значение параметра
                if x <= item[0]:
                    # c: итоговая оценка по параметру
                    c = item[1]
                    break
        
            _results[conclusion] = (x, c)
    
            # res: текст результата
            res += '[%s] <b>%s</b>\n' % (x, c)

    return res.strip()

def answer(bot, message, command, data=None, logger=None, question=None, **kw):
    """
        Make the step's answer
    """
    lang = kw.get('lang') or DEFAULT_LANGUAGE
    storage = kw.get('storage')
    name = kw.get('name')

    is_run = True

    if question == _QCOUNT or (IsDebug and question > 0 and question%10 == 0):
        result = get_result(storage, name, lang, mode=1)
        bot.send_message(message.chat.id, result, parse_mode=DEFAULT_PARSE_MODE)
        is_run = question < _QCOUNT

        if is_run:
            time.sleep(3)

    if question > _QCOUNT_EXT and 'query_id' in kw:
        if get_result(storage, name, lang, mode=2) and not storage.get(name, 'warning'):
            text = _WARNINGS[lang][0]

            bot.answer_callback_query(
                kw['query_id'],
                text=text,
                show_alert=True
                )

            storage.set(name, 'warning', 1)
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
        dbs.save_params(_test_name, _PARAMS, _results, **kw)

        if not _is_without_conclusions:
            dbs.save_conclusions(_test_name, _CONCLUSIONS, _results, **kw)
        """
        for p in sorted([x for x in _PARAMS[lang].keys()]):
            if p in _results:
                param = _PARAMS[lang][p][0]
                value, s1 = _results[p]
                storage.set(name, '%s.RP%s' % (_TEST_NAME, p), value)
                storage.set(name, '%s.TP%s' % (_TEST_NAME, p), '<i>%s</i>. %s:%s' % (param, s1, value), with_encode=True)

        if not _is_without_conclusions:
            conclusions = _CONCLUSIONS[lang]
            for conclusion in conclusions.keys():
                value, param = _results[conclusion]
                storage.set(name, '%s.RC' % _TEST_NAME, value)
                storage.set(name, '%s.TC%s' % (_TEST_NAME, conclusion), '%s:%s' % (param, value), with_encode=True)
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

def check(data, key, res):
    s = 0
    for k in data[key].keys():
        #print(k)
        q = k.split('.')[1]
        if not q.isdigit():
            continue
        #print(q)
        v = int(data[key][k])
        for i in range(0, 2):
            if int(q) in res[i]:
                s += i == 0 and v > 0 and 1 or i == 1 and v < 0 and 1 or 0
                break
    return s

def selftest(data, lang, with_print=None):
    key = _TEST_NAME
    params = dict([(k.split('.')[0], _PARAMS[lang][k]) for k in _PARAMS[lang].keys()])

    out = []
    r = {}
    for k in sorted(params.keys()):
        if not k in r:
            r[k] = 0
        x = check(data, key, params[k][2])
        if with_print:
            print(x)

        r[k] += x * params[k][1]

        rp = '%s.RP%s' % (key, k)
        if rp in data[key]:
            x = int(data[key].get(rp, '0'))
            if r[k] == x:
                out.append('OK')
            else:
                out.append('Error %s [%s:%s]' % (rp, r[k], x))
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
