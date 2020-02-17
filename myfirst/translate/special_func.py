from django.utils.http import is_safe_url, urlunquote
from urllib.parse import urlparse#разделяет наш полученный адрес по полычкам

# функция для получения ip___________________________________________
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    print('my ip')
    print(x_forwarded_for)
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
        print('if true')
        print(ip)
    else:
        ip = request.META.get('REMOTE_ADDR')
        print('if false')
        print(ip)
    return ip

# готовая функция переход на следующий url_________________________________________________
def get_next_url(request):
    # этот метод определяет полностью адрес с зоголовком. типа http://127.0.0.1:5000/translate/log/?next=/translate/signup/
    next = request.META.get('HTTP_REFERER')
    if next:
        next = urlunquote(next)  # HTTP_REFERER may be encoded.
    else:
    #if not is_safe_url(url=next, host=request.get_host()):
        next = '/'
    return next

# функция для получения отсеченного url - query 
def url_cut(request):

    n = request.META.get('HTTP_REFERER')#с помощью этого метода получаем полностью url адрес например:'http://127.0.0.1:5000/translate/log/translate/''
    next = urlparse(n).query
    next = next[5:]#здесь отсекаем не нужное
    print('done')
    return next

    # urlparse -- разделяет наш полученный адрес по полычкам например: 
    #ParseResult(scheme='http', netloc='127.0.0.1:5000', path='/translate/log/', para
    #ms='', query='next=/translate/', fragment='')
    # и здесь мы выбираем только query