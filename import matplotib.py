import matplotib.pyplot as pyplot

buah = ['Apel']['jeruk']['pisang']['anggur']
penjualan = [50,70,90,60]
plt.bar(buah, penjualan, color='skyblue')       
plt.title('diagram batang jumlah penjualan buah buahan')
plt.xlabel('buah')
plt.ylabel('jumlah penjualan')
plt.show()