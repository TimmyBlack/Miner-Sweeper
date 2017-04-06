from numpy import *
from scipy.signal import convolve2d
from time import *

class Board(object):
#内置函数
	def __init__(self,width=20,height=20,miner=40):
		self.width=width
		self.height=height
		self.miner=miner

		self.not_miner=width*height-miner
		#初始化非雷区域数

		self.board=ones(miner)
		self.board=append(self.board,zeros(self.not_miner))

		random.shuffle(self.board)
		#打乱雷数

		self.board=self.board.reshape(height,width)


		self.number=convolve2d(self.board,[[1,1,1],[1,10,1],[1,1,1]],'same')
		#雷数矩阵，用于表示每局游戏内置地雷分布状况

		self.know=-ones(width*height).reshape(height,width)
		#已知矩阵 用于表示已解开雷区

		self.statue=True
		#游戏状态 True为游戏中，False为游戏结束（失败）

		self.get_miner=0
		#初始化已知雷数为0

		self.get_know=0
		#初始化已知区域数为0

	def __str__(self):
		def __num2miner__(number,miner='●'):
			if number==-1:
				return '■'
			elif number==-2:
				return miner
			elif number>9:
				return miner
			elif number==0:
				return '  '
			return ' '+str(int(number))
		all=''
		for i in range(0,self.height):
			line=''
			for j in range(0,self.width):
				line+=__num2miner__(self.know[i][j])
			all+=line+'\n'
		all+='游戏状态:%s\n'%str(self.statue)
		all+='解开雷数:%d/%d'%(self.get_miner,self.miner)
		all+='已知数量:%d/%d'%(self.get_know,self.not_miner)
		return all


#装饰器
	def log(func):
		'''设置装饰器log,在执行每个click动作之后显示结果'''
		def wrapper(*args, **kw):
			func(*args, **kw)
			print(b)
		return wrapper


#判断函数
	def is_safe(self,x,y):
		'''定义函数is_safe,判断某未知处是否存在标错雷，或者是否为雷
	   未知，且不存在标错雷或存雷 返回 True
	   未知，但存在标错雷或存雷   返回 False
	   已知，                     返回 None
		'''
		if self.is_unknown(x,y):
			if self.know[x][y]==-1 and self.number[x][y]<10:
			#检查是否存雷
				return True
			elif self.know[x][y]==-2 and self.number[x][y]>=10:
			#检查是否正确标雷
				return True
			else:
				return False
		return None

	def is_unknown(self,x,y):
		'''定义函数is_unknown,判断此处是否未知'''
		return self.know[x][y]<0


#基本功能函数
	def show_safe(self,x,y):
		'''定义函数show_safe().令未知区域显示结果'''
		if self.know[x][y]<0:
		#仅在区域未知时执行操作
			if self.number[x][y]>9:
			#若为雷，返回为True，不执行操作
				return True
			elif self.number[x][y]>0:
			#若周围存雷，则仅点开此处
				self.know[x][y]=self.number[x][y]
				self.get_know+=1
			elif self.number[x][y]==0:
			#若周围不存雷，则点开周围全部
				self.know[x][y]=0
				self.get_know+=1
				self.around_func(x,y,self.show_safe)

	def mark_miner(self,x,y):
		'''定义函数mark_miner，实现标记某处为雷的功能'''
		self.know[x][y]=-2
		self.get_miner+=1

	def is_win(self):
		return (-1 not in self.know and self.get_miner==self.miner) or self.get_know==self.not_miner

	def end_game(self):
		'''定义函数end_game，实现游戏结束功能 显示全部雷区'''
		self.know=self.number
		self.statue=False

	def win_game(self):
		'''定义函数win_game，实现游戏胜利功能'''
		self.statue=False
		for x in range(self.height):
			for y in range(self.width):
				if self.is_unknown(x,y):
					self.mark_miner(x,y)
		print('!!!!!!!!!!!!!你赢了!!!!!!!!!!!!!')


#操作函数
	@log
	def left_click(self,x,y):
		'''定义函数left_click（左击）,实现左击功能'''
		if not self.statue:
		#判断游戏状态是否为结束，若为结束，则重新生成雷区
			self.__init__(self.width,self.height,self.miner)
		end=self.show_safe(x,y)
		if end:
		#若此处为雷（show_safe返回True）则结束游戏
			self.end_game()
		if self.is_win():
			self.win_game()

	@log
	def right_click(self,x,y):
		'''定义函数right_click（右击）,实现右击功能'''
		if self.is_unknown(x,y):
			self.mark_miner(x,y)
			if self.is_win():
				self.win_game()

	@log
	def both_click(self,x,y):
		'''定义函数both_click（双击左右键），实现排雷功能'''
		if self.around_func(x,y,self.is_safe)==self.around_func(x,y,self.is_unknown):
			self.around_func(x,y,self.show_safe)
			if self.is_win():
				self.win_game()

#高级函数
	def around_func(self,x,y,f):
		'''高级函数around_func,对坐标x,y周围的9个点做任意动作'''
		sum=0
		'''并统计数量'''
		for xx in range(x-1,x+2):
			if xx>=0 and xx<self.height:
			#统计是否在纵向区间内
				for yy in range(y-1,y+2):
					if yy>=0 and yy<self.width:
					#统计是否在横向区间内
						temp=f(xx,yy)
						if temp:
							sum+=1
		return sum
		#返回为True数量

#AI函数
	


if __name__=='__main__':
	b=Board(5,5,2)
	b.both_click(1,2)
