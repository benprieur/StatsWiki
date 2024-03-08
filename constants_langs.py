MONTHS_BY_LANG = { 
    'ar': 
    ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر'],
    'de' : 
    ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'],
    'en' : 
    ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
    'eo':
    ['Januaro', 'Februaro', 'Marto', 'Aprilo', 'Majo', 'Junio', 'Julio', 'Aŭgusto', 'Septembro', 'Oktobro', 'Novembro', 'Decembro'],
    'es' : 
    ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'],
    'fr' : 
    ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'],
    'he' : 
    ['ינואר', 'פברואר', 'מרץ', 'אפריל', 'מאי', 'יוני', 'יולי', 'אוגוסט', 'ספטמבר', 'אוקטובר', 'נובמבר', 'דצמבר'],
    'hy' : 
    ['Հունվար', 'Փետրվար', 'Մարտ', 'Ապրիլ', 'Մայիս', 'Հունիս', 'Հուլիս', 'Օգոստոս', 'Սեպտեմբեր', 'Հոկտեմբեր', 'Նոյեմբեր', 'Դեկտեմբեր'],
    'it' : 
    ['Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno', 'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre'],
    'ja' :
    ['1月 (いちがつ)', '2月 (にがつ)', '3月 (さんがつ)', '4月 (しがつ)', '5月 (ごがつ)', '6月 (ろくがつ)', '7月 (しちがつ)', '8月 (はちがつ)', '9月 (くがつ)', '10月 (じゅうがつ)', '11月 (じゅういちがつ)', '12月 (じゅうにがつ)'],
    'ko' :
    ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'],
    'nl' : 
    ['Januari', 'Februari', 'Maart', 'April', 'Mei', 'Juni', 'Juli', 'Augustus', 'September', 'Oktober', 'November', 'December'],
    'pl' :
    ['Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj', 'Czerwiec', 'Lipiec', 'Sierpień', 'Wrzesień', 'Październik', 'Listopad', 'Grudzień'],
    'pt' : 
    ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
    'ru' : 
    ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'],
    'uk' : 
    ['Січень', 'Лютий', 'Березень', 'Квітень', 'Травень', 'Червень', 'Липень', 'Серпень', 'Вересень', 'Жовтень', 'Листопад', 'Грудень'],
    'zh' : 
    ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月']
}

FILTERS_BY_LANG = {
    'global' :
        (
            'MediaWiki:', 
            '????:', 
            'Portal:', 
            'File:', 
            'Help:', 
            'Category:', 
            'Main_Page', 
            '�', 
            'User:', 
            'Template:', 
            'Special:', 
            'Wikipedia:',  
            'Catégorie:', 
            'Spécial:', 
            'Wikipédia', 
            'Project:',
            '404.php',
            'xss',
            'Orangemorange',
            'Wiki',
        ),
    'ar' :
        (
            'تصنيف:', 
            'خاص:', 
            'ويكيبيديا:', 
            'ويكيبيديا:',
            'الصفحة_الرئيسية',
            'ملف:',
        ),
    'de' : 
        (  
            'Kategorie:', 
            'Hauptseite', 
            'Spezial:', 
            'Benutzer:', 
            'Datei:'
        ),
    'en' : 
        (

        ),
    'eo' :
        (
            'Portalo:', 
            'Helpo:', 
            'Vikipedio:', 
            'Speciala', 
            'Uzanto:',
            'Kategorio:',
            'Vikipedia_diskuto:',
            'Ŝablono:',
            'XXX'
        ),    
    'es' : 
        (
            'Especial:',
            'Archivo:'
        ),
    'fr' : 
        (

            'Accueil', 
            'Wikip�', 
            'Sp?cial:', 
            'Fichier:', 
            'Aide:',
            'Cookie_(informatique)'
        ),
    'he' : 
        (
            'משתמש:', 
            'קובץ:', 
            'עמוד_ראשי', 
            'מיוחד:', 
            'ויקיפדיה:'
        ),
    'hy' : 
        (
            'Կաղապար:', 
            'Վիքիպեդիա:', 
            'Կատեգորիա:', 
            'Գլխավոր_էջ', 
            'Ստորոգութիւն:', 
            'Սպասարկող:',
            'Վիքինախագիծ:',
            'Մասնակից:'
         ),
    'ko' : 
        (
            '특수:', 
            '최근_바뀜',
            '위키백과:', 
            '특수:',
            '폰허브'
        ),    
    'it' :
        (
            'Pagina', 
            'Speciale:'
        ),
    'ja' :
        (
            'メインページ', 
            '特別:', 
            'Re:'
        ),
    'nl' : 
        (
            'Hoofdpagina', 
            'Speciaal:'
        ),
    'pl':
        (
            'Specjalna:', 
            'Strona_główna',
            'Szablon:',
            'Plik:'
        ),
    'pt' : 
        (
            'Usuário(a) Discussão:', 
            'Wikip�', 
            'Especial:', 
            'Ficheiro:', 
            'Predefinição:'
        ),
    'ru' :
        (
            'Категория:',
            'Википедия:',
            'Первый мститель:', 
            'Заглавная_страница', 
            'Служебная:', 
        ),
    'uk' : 
        (
            'Дюна:', 
            'Файл:', 
            'Спеціальна:', 
            'Вікіпедія:', 
            'Головна_сторінка'
        ),
    'zh' : 
        (
            '維基媒體基金會', 
            '首页'
        )    
}

GlOBAL_PAGE_STUFF = {
    'ar':
        {
            'title': 'ويكيبيديا بالعربية',
            'title_article': 'مقالة',
            'title_views': 'المشاهدات'
        },
    'de' :
        {
            'title': 'Wikipedia auf Deutsch',
            'title_article': 'Artikel',
            'title_views': 'Aufrufe'
        },
    'en' : 
        {
            'title': 'Wikipedia in English', 
            'title_article': 'Article', 
            'title_views': 'Views'
        },
    'eo' : 
        {
            'title': 'Vikipedio en Esperanto',
            'title_article': 'Artikolo',
            'title_views': 'Vidoj'
        },
    'es' :
        {
            "title": "Wikipedia en Español",
            "title_article": "Artículo",
            "title_views": "Vistas"
        },    
    'fr' : 
        {
            'title': 'Wikipédia en français', 
            'title_article': 'Article', 
            'title_views': 'Vues'
        },
    'he' :
        {
            'title': 'ויקיפדיה בעברית',
            'title_article': 'מאמר',
            'title_views': 'צפיות'
        },
    'hy' :
        {
            'title': 'Վիքիպեդիան հայերենով', 
            'title_article': 'Հոդված', 
            'title_views': 'Դիտումներ'
        },
    'it' :
        {    
            'title': 'Wikipedia in italiano',
            'title_article': 'Articolo',
            'title_views': 'Visualizzazioni'
        },
    'ja' :
        {
            "title": "日本語のウィキペディア",
            "title_article": "記事",
            "title_views": "閲覧数"
        },
    'ko' : 
        {
            'title': '한국어 위키백과', 
            'title_article': '기사', 
            'title_views': '조회수'
        },                       
    'nl' :
        {
            'title': 'Wikipedia in het Nederlands',
            'title_article': 'Artikel',
            'title_views': 'Weergaven'
        },
    'pl' : 
        {
            'title': 'Wikipedia po polsku', 
            'title_article': 'Artykuł', 
            'title_views': 'Wyświetlenia'
        },
    'pt' : 
        {
            'title': 'Wikipédia em português',
            'title_article': 'Artigo',
            'title_views': 'Visualizações'
        },
    'ru' : 
        {
            'title': 'Википедия на русском', 
            'title_article': 'Статья', 
            'title_views': 'Просмотры'
        },
    'uk' :
        {
            'title': 'Вікіпедія українською', 
            'title_article': 'Стаття', 
            'title_views': 'Перегляди'
        },
    'zh': 
        {
            'title': '中文维基百科', 
            'title_article': '文章', 
            'title_views': '浏览量'
        }      
    }

FLAGS_STUFF = {
    'ar': 
    "<img src='/static/ar.svg' style='height: 10px; width: auto;'>",
    'de': 
    "<img src='/static/de.svg' style='height: 10px; width: auto;'>",
    'en': 
    "<img src='/static/en-uk.svg' style='height: 10px; width: auto;'><img src='/static/en-us.svg' style='height: 10px; width: auto;'>",
    'eo': 
    "<img src='/static/eo.svg' style='height: 10px; width: auto;'>",
    'es': 
    "<img src='/static/es.svg' style='height: 10px; width: auto;'><img src='/static/es-me.svg' style='height: 10px; width: auto;'>",
    'fr': 
    "<img src='/static/francophonie.svg' style='height: 10px; width: auto;'><img src='/static/fr.svg' style='height: 10px; width: auto;'>",
    'he': 
    "<img src='/static/he.svg' style='height: 10px; width: auto;'>",
    'hy': 
    "<img src='/static/artsakh.svg' style='height: 10px; width: auto;'>",
    'it': 
    "<img src='/static/it.svg' style='height: 10px; width: auto;'>",
    'ja': 
    "<img src='/static/ja.svg' style='height: 10px; width: auto;'>",
    'ko': 
    "<img src='/static/ko.svg' style='height: 10px; width: auto;'>",
    'nl': 
    "<img src='/static/nl.svg' style='height: 10px; width: auto;'>",
    'pl': 
    "<img src='/static/pl.svg' style='height: 10px; width: auto;'>",
    'pt': 
    "<img src='/static/pt-pt.svg' style='height: 10px; width: auto;'><img src='/static/pt-br.svg' style='height: 10px; width: auto;'>",
    'ru': 
    "<img src='/static/ru.svg' style='height: 10px; width: auto;'>",
    'uk': 
    "<img src='/static/uk.svg' style='height: 10px; width: auto;'>",
    'zh': 
    "<img src='/static/zh.svg' style='height: 10px; width: auto;'>"
}

YEAR_PAGE_STUFF = {
    'ar': {
        'bymonthyear': "حسب شهر السنة",
    },
    'de': {
        "bymonthyear": "Nach Monat des Jahres",
    },
    'en': {
        'bymonthyear': "By month of the year",
        },
    'eo': {
        'bymonthyear': "Laŭ monato de la jaro",         
    },        
    'es': {
        'bymonthyear': "Por mes del año",
        },
    'fr': {        
        'bymonthyear': "Par mois de l'année", 
        },
    'he': {
        'bymonthyear': "לפי חודש בשנה",
    },
    'hy': {
        'bymonthyear': "Տարվա ամսերով",
    },
    'it': {
        'bymonthyear': "Per mese dell'anno",
    },
    'ja': {
        'bymonthyear': "年間の月別",
    },
    'ko': {
        'bymonthyear': "연도별 월별",
    },
    'nl': {
        "bymonthyear": "Per maand van het jaar",
    },
    'pl': {
        'bymonthyear': "Według miesiąca roku",
    },    
    'pt': {
        'bymonthyear': "Por mês do ano",
    },
    'ru': {
        'bymonthyear': "По месяцам года",
    },
    'uk': {
        'bymonthyear': "За місяцями року",     
    },
    'zh': {
        'bymonthyear': "按年份的月份",
    }
}
 
MONTH_PAGE_STUFF = {
    'ar': {
        'byday': "حسب يوم من الشهر",
    },
    'de': {
        "byday": "Nach Tag des Monats",
    },
    'en': {
        'byday': "By day of month",  
    },
    'eo': {
        'byday': "Laŭ tago de la monato",
    },
    'es': {
        'byday': "Por día del mes",
    },
    'fr': {
        'byday': "Par jour du mois", 
    },
    'he': {
        'byday': "לפי יום בחודש",
    },
    'hy': {
        'byday': "Ամսվա օրերով", 
    },
    'it': {
        'byday': "Per giorno del mese",
    },
    'ja': {
        'byday': "月の日別",
    },
    'ko': {
        'byday': "월별 일자별",
    },
    'nl': {
        "byday": "Per dag van de maand",
    },
    'pl': {
        'byday': "Według dnia miesiąca",
    },    
    'pt': {
        'byday': "Por dia do mês",
    },
    'ru': {
        'byday': "По дням месяца",
    },
    'uk': {
        'byday': "По днях місяця",
    },
    'zh': {
        'byday': "按月份中的日",
    }
}

DAILY_TWEET_SENTENCE = {
    'ar': 'المقالات الأكثر استشارة على ar.wikipedia يوم أمس',
    'de': 'Meistgesehene Artikel auf de.wikipedia gestern',
    'en': 'Articles en.wikipedia the most consulted yesterday',
    'eo': 'Artikoloj en eo.wikipedia plej konsultitaj hieraŭ',
    'es': 'Artículos es.wikipedia más consultados ayer',
    'fr': 'Articles fr.wikipedia les plus vus hier',
    'he': 'מאמרים ב-he.wikipedia שזכו לצפייה הרבה ביותר אתמול',
    'hy': 'Հյուրագրված հոդվածներ hy.wikipedia-ում երեկ',
    'it': 'Articoli di it.wikipedia più visualizzati ieri',
    'ja': '昨日最も閲覧されたja.wikipediaの記事',
    'ko': '어제 가장 많이 조회된 ko.wikipedia의 기사들',
    'nl': 'Meest bekeken artikelen op nl.wikipedia gisteren',
    'pl': 'Artykuły na pl.wikipedia najczęściej konsultowane wczoraj',
    'pt': 'Artigos mais vistos ontem na pt.Wikipedia',
    'ru': 'Самые консультируемые статьи на ru.wikipedia вчера',
    'uk': 'Статті uk.wikipedia найбільш консультовані вчора',
    'zh': '昨天在zh.wikipedia上咨询最多的文章'
}

MONTHLY_TWEET_SENTENCE = {
    'ar': 'المقالات الأكثر استشارة على ar.wikipedia',
    'de': 'Meistgesehene Artikel auf de.wikipedia',
    'en': 'Articles en.wikipedia the most consulted',
    'eo': 'Artikoloj en eo.wikipedia plej konsultitaj',
    'es': 'Artículos más consultados en es.wikipedia',
    'fr': 'Articles fr.Wikipedia les plus vus',
    'he': 'מאמרים ב-he.wikipedia הכי נצפים',
    'hy': 'Հյուրագրված հոդվածներ hy.wikipedia-ում երեկ',
    'it': 'Articoli più visualizzati su it.wikipedia',
    'ja': 'ja.wikipediaで最も閲覧された記事',
    'ko': 'ko.wikipedia에서 가장 많이 조회된 기사들',
    'nl': 'Meest bekeken artikelen op nl.Wikipedia',
'    pl': 'Najczęściej konsultowane artykuły na pl.wikipedia',    
    'pt': 'Artigos mais vistos ontem na pt.Wikipedia',
    'ru': 'Самые консультируемые статьи на ru.wikipedia',
    'uk': 'Статті uk.wikipedia найбільш консультовані вчора',
    'zh': '在zh.wikipedia上最多咨询的文章'
}

SUPPORTED_REDIRECTS_BY_LANG = { 
    'ar': 
        {
            'قائمة الدول_والتبعيات حسب_عد السكان' : 'Q712280'
        },
    'de': 
        {

        },
    'en': 
        {
            '2019–20coronavirus pandemic' : 'Q81068910'
        }, 
    'eo': 
        {
            'Kreo' : 'Q215304'
        },
    'es': 
        {

        },
    'fr': 
        {
            "Pandémie de maladie à coronavirus de 2019-2020" : "Q81068910",
            
            "Pandémie de maladie à coronavirus de 2020 en France" : "Q83873593",
            
            "Grippe de 1918" : "Q178275",
            
            "Charles de Galles" : "Q43274",

            "Mort de George Floyd" : "Q95579249",

            "Cédric Doumbé" : "Q24452252",

            "Coupe d'Afrique des Nations" : "Q83145"
        },
    'ja': 
        {

        },
    'he': 
        {

        },
    'hy': 
        {
            'ערים בישראל' : 'Q28330'
        },
    'it': 
        {

        },
    'ko': 
        {

        },
    'nl': 
        {
            'Google Inc.' : "Q95"
        },
    'pl': 
        {

        },
    'pt': 
        {

        },
    'ru': 
        {

        },
    'uk': 
        {
            'Російське вторгнення в Україну (2022)' : 'Q110999040'
        },
    'zh': 
        {

        }
}