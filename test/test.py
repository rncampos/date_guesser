from date_guesser_rc import guess_date
import datetime
import pytz

def test_parse_urls_with_date():
    test_urls = (
        ('2021-04-24 00:00:00', 'https://tvi24.iol.pt/internacional/24-04-2021/iraque-incendio-em-unidade-de-cuidados-intensivos-faz-23-mortos'),
        ('2021-04-24 00:00:00', 'https://tvi24.iol.pt/internacional/24/04/2021/iraque-incendio-em-unidade-de-cuidados-intensivos-faz-23-mortos'),
        ('2021-04-24 00:00:00', 'https://expresso.pt/economia/2021-04-24-Quem-ganhou-e-perdeu-nas-negociacoes-da-bazuca--84c43f2b'),
        ('2016-05-09 18:43:07', 'https://arquivo.pt/noFrame/replay/20160509184307/http://www.tvi24.iol.pt/tecnologia/mercurio/fenomeno-raro-nos-ceus-pode-ser-hoje-observado-em-portugal'),
        ('2021-04-24 00:00:00', 'https://arquivo.pt/noFrame/replay/20160509184307/https://tvi24.iol.pt/internacional/24/04/2021/iraque-incendio-em-unidade-de-cuidados-intensivos-faz-23-mortos'),
        ('2017-03-23 00:00:00', 'https://arquivo.pt/wayback/20170401205010/http://expresso.sapo.pt/revista-de-imprensa/2017-03-23-Banco-de-Portugal-podia-ter-retirado-idoneidade-a-Ricardo-Salgado-em-2013'),
        ('2013-12-16 00:00:00', 'http://www.news.com/20131216/beyonce-album_n_4453500.html'),
        ('2015-10-15 00:00:00', 'http://www.news.com/local/2015/10/jim_webb'),
        ('2016-2-15 00:00:00', 'http://news.org/1/files/2016-02/ohio-FY2014-15-budget.pdf#page=5'),
        ('2021-04-25 00:00:00', 'https://www.theguardian.com/world/live/2021/apr/25/covid-live-indian-pm-narendra-modi-storm-of-coronavirus-infections-has-shaken-country-latest-updates'),
        ('2013-01-15 00:00:00', 'http://www.news.com/2013/jan/beyonce-album_n_4453500.html'),
        ('2013-09-15 00:00:00', 'http://www.news.com/sept/2013/beyonce-album_n_4453500.html'),
        ('2013-12-17 00:00:00', 'http://www.cnn.com/12/17/2013/politics/senate/index.html?hpt=hp_t1'),
        ('2013-12-17 00:00:00', 'http://www.cnn.com/2013/12/17/politics/senate/index.html?hpt=hp_t1'),
    )
    for date_str, url in test_urls:
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.utc)
        guess = guess_date(url)
        print(guess.date)
        assert guess.date == date

def test_parse_tricky_urls():
    test_urls_no_date = (
        'http://chriskeniston2016.com/3385-2/',  # 2016.com parses as 'YEAR.month'
        'http://www.news.co/libro-198781',  # if this ends in '199781', parses to 08/01/1997
        'http://www.news.co/libro-205081',
        'http://www.news.co/libro-201008012',  # the extra '2' means not '08/01/2010'
        'http://www.news.com/2013/13/22/beyonce-album_n_4453500.html',  # 13 months?
        'http://www.news.com/2013/01/32/beyonce-album_n_4453500.html',  # 32 days?
        'http://www.news.com/2013/02/29/beyonce-album_n_4453500.html',  # 2013 not a leap year
    )
    for url in test_urls_no_date:
        guess = guess_date(url)
        print(guess.date)
        assert guess.date is None

def test_filter_url_for_undateable():
    test_urls_undateable = (
        '/foo/bar/baz.html',  # no hostname
        'https://new.project.in.en.wikipedia.org/other_stuff',  # any wikipedia subdomain
        'https://twitter.com/',  # twitter homepage
        'https://mobile.twitter.com/nytimes',  # twitter user feeds
        'https://twitter.com/hashtag/MITLegalForum',  # twitter hashtag feeds
        'https://foo.bar.com/',  # any front page
        'https://www.google.es/search?q=chocolate',  # search terms
        'http://www.medianama.com/tag/aadhaar-act',  # tag pages
    )

    for url in test_urls_undateable:
        guess = guess_date(url)
        print(guess.date)
        assert not (guess is None)


test_parse_urls_with_date()
test_parse_tricky_urls()
test_filter_url_for_undateable()
#guess = guess_date(url='https://arquivo.pt/noFrame/replay/20160509192028/http://www.tvi24.iol.pt/tecnologia/mercurio/fenomeno-raro-nos-ceus-pode-ser-hoje-observado-em-portugal')
#print(guess.date)