"""Q8 Matrix maximum-score path and count. Moves: right, down, diagonal."""
import sys
MOD=1_000_000_007
def solve(grid):
    n=len(grid); m=len(grid[0])
    if grid[0][0] is None or grid[-1][-1] is None:return "IMPOSSIBLE"
    prev=[None]*m; prev_count=[0]*m
    for i in range(n):
        cur=[None]*m; counts=[0]*m
        for j in range(m):
            v=grid[i][j]
            if v is None:continue
            if i==j==0:cur[j]=v; counts[j]=1; continue
            candidates=[]
            if j and cur[j-1] is not None:candidates.append((cur[j-1],counts[j-1]))
            if i and prev[j] is not None:candidates.append((prev[j],prev_count[j]))
            if i and j and prev[j-1] is not None:candidates.append((prev[j-1],prev_count[j-1]))
            if candidates:
                best=max(x[0] for x in candidates); cur[j]=best+v
                counts[j]=sum(c for score,c in candidates if score==best)%MOD
        prev,prev_count=cur,counts
    return "IMPOSSIBLE" if prev[-1] is None else f"{prev[-1]} {prev_count[-1]}"
def main():
    try:
        a=sys.stdin.read().split(); n,m=int(a[0]),int(a[1])
        if not 1<=n<=2000 or not 1<=m<=2000 or len(a)!=2+n*m:raise ValueError("Invalid dimensions or cell count")
        grid=[]; k=2
        for _ in range(n):
            row=[]
            for _ in range(m): row.append(None if a[k].upper()=="X" else int(a[k])); k+=1
            grid.append(row)
        print(solve(grid))
    except (ValueError,IndexError) as e:raise SystemExit(f"Input error: {e}")
if __name__=="__main__":main()
