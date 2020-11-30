import sys
import urllib.request

def main():
    months = ['open', 'feb', 'jan', 'dec']
    divs = ['gold', 'silver', 'bronze']

    
    for div in divs:
        with open(f"{div}.txt", "w") as f:
            for year in range(20, 15, -1):
                for month in months:
                    _year = year
                    if month == 'dec':
                        _year -= 1
                    print('http://usaco.org/current/data/'
                            f'{month}{_year}_{div}_results.html')
                    url = urllib.request.urlopen('http://usaco.org/current/data/'
                            f'{month}{_year}_{div}_results.html')
                    for line in url.readlines():
                        _line = str(line)
                        if "<tr><td>" in _line:
                            f.write(_line + '\n')

if __name__ == "__main__":
    main()
