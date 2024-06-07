import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from matplotlib.animation import FuncAnimation

# 假设我们有一个函数可以实时获取光标的位置
def get_cursor_position():
    # 模拟光标移动数据（例如：随机生成）
    t = np.linspace(0, 10, 100)
    x = 2 * t + np.random.normal(0, 0.5, size=t.size)
    y = 3 * t**2 + np.random.normal(0, 10, size=t.size)
    return t, x, y

# 获取光标位置数据
t, x, y = get_cursor_position()

# 定义二次多项式模型
def polynomial_model(t, a, b, c):
    return a * t**2 + b * t + c

# 对 x 和 y 位置分别进行拟合
params_x, _ = curve_fit(polynomial_model, t, x)
params_y, _ = curve_fit(polynomial_model, t, y)

# 使用拟合参数计算拟合结果
x_fit = polynomial_model(t, *params_x)
y_fit = polynomial_model(t, *params_y)

# 创建图形和子图
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

# 初始化子图
ax1.set_xlim(0, 10)
ax1.set_ylim(min(x) - 1, max(x) + 1)
ax1.set_xlabel('Time')
ax1.set_ylabel('X Position')
ax1.set_title('X Position Over Time')
line1, = ax1.plot([], [], lw=2, label='Fitted x')
scat1 = ax1.scatter([], [], label='Original x')
ax1.legend()

ax2.set_xlim(0, 10)
ax2.set_ylim(min(y) - 10, max(y) + 10)
ax2.set_xlabel('Time')
ax2.set_ylabel('Y Position')
ax2.set_title('Y Position Over Time')
line2, = ax2.plot([], [], lw=2, label='Fitted y')
scat2 = ax2.scatter([], [], label='Original y')
ax2.legend()

# 初始化动画函数
def init():
    line1.set_data([], [])
    scat1.set_offsets([])
    line2.set_data([], [])
    scat2.set_offsets([])
    return line1, scat1, line2, scat2

# 更新动画函数
def update(frame):
    line1.set_data(t[:frame], x_fit[:frame])
    scat1.set_offsets(np.c_[t[:frame], x[:frame]])
    line2.set_data(t[:frame], y_fit[:frame])
    scat2.set_offsets(np.c_[t[:frame], y[:frame]])
    return line1, scat1, line2, scat2

# 创建动画
ani = FuncAnimation(fig, update, frames=len(t), init_func=init, blit=True)

plt.show()