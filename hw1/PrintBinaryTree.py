import math as math
import tabulate_cell_merger.tabulate_cell_merger as tab    

#SPRUHA:method to print a binary tree using tabulate cell merger package - needs to be imported using pip install tabulate_cell_merger
def print_list_as_binary_tree(fromlist):
    size=len(fromlist)
    depth=math.ceil(math.log2(size+1))
    maxwidth=2**(depth-1)
    index=0
    tableforprinting=[]
    columnstomerge={}
    for i in range(1,depth+1):
        paddingsize=2**(depth-i)-1
        padding=['']*paddingsize
        rowindex=i-1
        colindex=0
        rowlist=[]
        index=2**(i-1)-1
        for j in range(index,min(size,(2**i-1))):
            rowlist.append(fromlist[j])
            rowlist=rowlist+padding
            columnstomerge[(rowindex,colindex)]=paddingsize+1
            colindex=colindex+paddingsize+1
        tableforprinting.append(rowlist)
    print(tab.tabulate(tableforprinting,columnstomerge))