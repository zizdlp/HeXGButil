from  HeXGButil.HeXGButil import forgrad,split4bin,digitize4int, digitize4float
import numpy as np

def test_digitize4float():
    x=np.array([1,2,3],dtype="float32")
    y=np.array([1],dtype="float32")
    res=digitize4float(x,y)
    true_res = np.array([0,1,1],dtype="uint16")
    assert(len(res)==len(true_res))
    for i in range(len(res)):
        assert(res[i]==true_res[i])
def test_digitize4int():
    x=np.array([1,2,3],dtype="uint16")
    y=np.array([1],dtype="uint16")
    res=digitize4int(x,y)
    true_res = np.array([0,1,1],dtype="uint8")
    assert(len(res)==len(true_res))
    for i in range(len(res)):
        assert(res[i]==true_res[i])
def test_split4bin():
    n_samples, split_bins, discrete_x, insts, node_index_list=3,3,np.array([1,2,3],dtype="uint16"),np.array([1,2,3],dtype="int32"),np.array([1,2,3],dtype="int32")
    res1,res2=split4bin(n_samples, split_bins, discrete_x, insts, node_index_list)
    true_res1=np.array([5,8,9],dtype="uint8")
    true_res2=np.array([[65535],[65535],[65535]],dtype="uint16")
    assert(len(res1)==len(true_res1))
    for i in range(len(res1)):
        assert(res1[i]==true_res1[i])
    assert(len(res2)==len(true_res2))
    for i in range(len(res2)):
        for j in range(len(res2[i])):
            assert(res2[i][j]==true_res2[i][j])
def test_forgrad():
    binss,ghs,split_bins,n_nodes,i= np.array([1,2,3],dtype="uint8"),np.array([1,2,3],dtype="uint32"),1,1,1
    res=forgrad(binss,ghs,split_bins,n_nodes,i)
    true_res=np.array([[0,0]],dtype="float32")
    assert(len(res)==len(true_res))
    for i in range(len(res)):
        for j in range(len(res[i])):
            assert(res[i][j]==true_res[i][j])
if __name__ == "__main__":
    print("HeXGButil test start:")
    test_digitize4float()
    test_digitize4int()
    test_forgrad()
    test_split4bin()
    print("HeXGButil test succ")