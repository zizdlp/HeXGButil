from numba.pycc import CC
import numpy as np
cc = CC('HeXGButil')
# Uncomment the following line to print out the compilation steps
#cc.verbose = True


@cc.export('digitize4float','uint16[:](float32[:],float32[:])')
def digitize4float(xs,splits): ####右边界
    output=np.zeros(len(xs),dtype='uint16')
    for k in range(len(xs)):
        x=xs[k]
        l,r=0,len(splits)   ####[l,r]
        while(l<r):
            m=(l+r)>>1
            if splits[m]<x:
                l=m+1
            elif splits[m]==x:
                l=m
                r=m
            else:
                r=m
        output[k]=l
    return output

@cc.export('digitize4int','uint8[:](uint16[:],uint16[:])')
def digitize4int(xs,splits): ####右边界
    output=np.zeros(len(xs),dtype='uint8')
    for k in range(len(xs)):
        x=xs[k]
        l,r=0,len(splits)   ####[l,r]
        while(l<r):
            m=(l+r)>>1
            if splits[m]<x:
                l=m+1
            elif splits[m]==x:
                l=m
                r=m
            else:
                r=m
        output[k]=l
    return output


@cc.export('split4bin','(int32,int32,uint16[:],int32[:],int32[:])')
def split4bin(n_samples, split_bins, discrete_x, insts, node_index_list):
    n_nodes = len(node_index_list)
    bins = np.zeros(n_samples, dtype='uint8')

    ma = discrete_x.max()+1
    mi=discrete_x.min()
    temp = np.zeros((n_nodes, ma)).astype(np.int32)
    total_sum = np.zeros(n_nodes).astype(np.int32)
    for idx, item in enumerate(discrete_x):
        cur_node = insts[idx]
        temp[cur_node][item] += 1
        total_sum[cur_node] += 1
    splitss= np.zeros((n_nodes,split_bins), dtype='uint16')
    cur_loc=np.zeros(n_nodes,dtype='int32')  ###[0,cur_loc)
    for i in range(n_nodes):
        the_bin_pre = -1
        cum = 0
        first=-1
        last=-1
        last_2=-1
        for j in range(mi,ma):
            if temp[i][ma-j-1]>0:
                if last==-1:
                    last=ma-j-1
                elif last_2==-1:
                    last_2=ma-j-1
            if temp[i][j] > 0:
                if first==-1:
                    first=j
                cum+=temp[i][j]
                the_bin = cum*split_bins//total_sum[i]
                if the_bin != the_bin_pre:
                    if the_bin_pre==-1:
                        the_bin_pre=the_bin
                    else:
                        splitss[i][cur_loc[i]]=j
                        cur_loc[i]+=1
                        the_bin_pre = the_bin
        cur_loc[i]-=1

        if  splitss[i][0]!=first and cur_loc[i]<split_bins-1:
            splitss[i][cur_loc[i]]=first
            cur_loc[i]+=1
            if (splitss[i][cur_loc[i]-2]!=last_2 and cur_loc[i]<split_bins-1):
            
                splitss[i][cur_loc[i]]=last_2
                cur_loc[i]+=1
        elif (splitss[i][cur_loc[i]-1]!=last_2 and cur_loc[i]<split_bins-1):
            splitss[i][cur_loc[i]]=last_2
            cur_loc[i]+=1
    for i in range(n_samples):
        cur_node = insts[i]
        if cur_node >= 0:
            cur_splits = splitss[cur_node]
            x = discrete_x[i]
            l, r = 0, len(cur_splits)  # [l,r]
            while(l < r):
                m = (l+r)//2
                if cur_splits[m] < x:
                    l = m+1
                elif cur_splits[m] == x:
                    l = m
                    r = m
                else:
                    r = m
            bins[i] = l+cur_node*split_bins
    return bins,[splitss[i,:cur_loc[i]]  for i in range(splitss.shape[0])]


@cc.export('forgrad','float32[:,:](uint8[:,:],float32[:,:],int32,int32,int32)')
def forgrad(binss,ghs,split_bins,n_nodes,i):
    gh_sum = np.zeros((split_bins * n_nodes, 2),dtype=np.float32)
    for k in range(len(binss)):
        if binss[k,i]>=0:
            gh_sum[binss[k,i]][0]+=ghs[k][0]
            gh_sum[binss[k,i]][1]+=ghs[k][1]
    return gh_sum   

if __name__ == "__main__":
    cc.compile()

