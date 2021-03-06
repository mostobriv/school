import urllib.request
import bs4 as bs

''' 
	метод urlopen() возвращает объект, у которого есть метод read(), 
	который возвращает исходный текст страницы. Собственно исходный текст страницы 
	мы и складываем в переменную source.
'''
source = urllib.request.urlopen("нужно самим вставить сюда ссылку").read()

'''
	Но если вы выведите содержимое переменной source в консоль, то увидите, что код будет некрасиво форматирован.
	Чтобы сделать вывод примерно как в браузере, ну и на самом деле для дальнейшей работы, мы воспользуемся 
	библиотекой BeautifulSoup. 
'''
soup = bs.BeautifulSoup(source, 'lxml')

'''
	Теперь мы можем начинать собирать нужную нам информацию. 
	Заметим, что описание каждой пиццы имеет одну и ту же структуру. 
	Т.е каждую такую структуру мы можем сохранить в список и в дальнейшем написать код для одной пиццы,
	а итерируясь по списку, получить данные для всех.

	С помощью метода find_all() из модуля BeautifulSoup, по тегам мы можем выбрать нужные куски html-кода.
	Т.е метод найдет все кусочки html-кода, которые заключены в теге с <div class='product-item-main product-clickable'> ... </div>.
	В итоге в переменной products будут такие кусочки кода для каждой пиццы.
'''
products = soup.find_all('div', {"class": "product-item-main product-clickable"})

'''
	Далее мы уже готовы к тому, чтобы начать собирать нужную информацию.
	Сохранять ее будем в переменную типа словарь, где ключом будет название пиццы, а значением - список, где первый элемент - цена, а второй - калории.
'''
# pizza = {'pizza_name' : [price, energy]}
pizza = {}


for product in products:
	'''
		Т.к в products у нас лежит список из html-кода с информацией для каждой пиццы, то итерируемся по каждой пицце и
		с помощью уже знакомого метода библиотеки находим сначала имя.

		Если посмотреть по исходному коду страницы, то можно заметить, что наименовании пиццы лежит в теге
		<div class="link-detail"> Some name </div>. Метод find_all() возвращает нам список, но в коде имя одно, поэтому мы
		берем первый элемент с помощью [0], и нам нужно само имя, а не все определение тега, поэтому воспользуемся методом get_text(),
		который из тега достанет имя пиццы.
	'''	
	name = product.find_all('div', {"class" : "link-detail"})[0].find_all('span', {'itemprop' : 'name'})
	name = name[0].get_text()
	
	'''
		Далее можем заметить, что в блоке находится информация как для большой пиццы, так и для маленькой.
		Мы решили, что нам интересны большие!

		Находим интересующий нас блок кода с ценой.
	'''
	medium_pizza = product.find_all('div', {"class" : "value-price"})
	
	'''
		В переменной medium_pizza у нас два значения: для маленькой и для большой.
		Т.к нам нужна большая, а она находится в списке на втором месте, то обращаемся берем это значения обращаясь через [1]
		и воспользовавшись методов get_text() получаем текст, а не тэг.
		Видим, что в тексте много пробелов вокруг и к цене добавлен символ 'P'. Т.к нам нужно будет строку перевести в число,
		то нам необходимо избавиться от лишних пробелов по краям с помощью метода строк strip(), а чтобы убрать ненужный символ, 
		то мы просто можем заменить его на ничего. 
	'''
	price = medium_pizza[1].get_text().strip().replace("P","")
	'''
		Так же достаем строку с указанием количества калорий. Видим, что в строке возвращается '1286 ккал 805 гр', а нам
		нужно только первое число. Мы можем строку разделить относительно пробелов и получить список из слов. Тогда количество
		калорий в списке будет на первом месте и мы можем обратиться к этому элементу как к элементу списка [0].
	'''
	energy = product.find_all('div', {"class" : "item-energy"})[1].get_text().split()[0]

	'''
		Собственно складываем в словарь по имени пиццы список, в котором цена и калории.
	'''
	pizza[name] = [int(price), int(energy)]

	'''
		И так проделываем для каждого элемента-пиццы из списка products
	'''

	
'''
	Теперь нам нужно найти максимальное отношение калорий к цене. 
	Теперь уже простая задача, с которой вы вероятно уже сталкивались не раз :)
'''	

#print(pizza)
maximum = 0
pizza_name = ''
for name, attribute in pizza.items():
	""" Каллорий должно быть больше, а цена меньше"""
	val = attribute[1] / attribute[0]
	if val > maximum:
		maximum = val
		pizza_name = name
	#print(name, attribute[0] / attribute[1])

print(name, maximum)
