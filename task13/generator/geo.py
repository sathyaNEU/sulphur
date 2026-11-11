"""Point to line-segment distances through a grid index."""
import numpy as np
import pandas as pd


class SegIndex:
    def __init__(self, S, cell=1.0):
        self.S = S
        self.cell = cell
        x0, y0, x1, y1 = S.x0.values, S.y0.values, S.x1.values, S.y1.values
        self.a = np.c_[x0, y0]
        self.b = np.c_[x1, y1]
        cx = np.floor(np.minimum(x0, x1) / cell).astype(int)
        cy = np.floor(np.minimum(y0, y1) / cell).astype(int)
        cx2 = np.floor(np.maximum(x0, x1) / cell).astype(int)
        cy2 = np.floor(np.maximum(y0, y1) / cell).astype(int)
        grid = {}
        for i in range(len(S)):
            for gx in range(cx[i] - 1, cx2[i] + 2):
                for gy in range(cy[i] - 1, cy2[i] + 2):
                    grid.setdefault((gx, gy), []).append(i)
        self.grid = {k: np.array(v) for k, v in grid.items()}

    def near(self, px, py, rmax):
        """all (point, segment, distance in km) with distance <= rmax (rmax <= cell)"""
        px = np.asarray(px, float)
        py = np.asarray(py, float)
        gx = np.floor(px / self.cell).astype(int)
        gy = np.floor(py / self.cell).astype(int)
        key = pd.Series(list(zip(gx, gy)))
        out_p, out_s, out_d = [], [], []
        for k, idx in key.groupby(key).groups.items():
            segs = self.grid.get(k)
            if segs is None:
                continue
            pi = np.asarray(list(idx))
            P = np.c_[px[pi], py[pi]]
            A = self.a[segs]
            B = self.b[segs]
            AB = B - A
            L2 = np.maximum((AB ** 2).sum(1), 1e-12)
            AP = P[:, None, :] - A[None, :, :]
            t = np.clip((AP * AB[None]).sum(2) / L2[None], 0, 1)
            C = A[None] + t[..., None] * AB[None]
            d = np.hypot(P[:, None, 0] - C[..., 0], P[:, None, 1] - C[..., 1])
            ii, jj = np.where(d <= rmax)
            out_p.append(pi[ii])
            out_s.append(segs[jj])
            out_d.append(d[ii, jj])
        if not out_p:
            return np.array([], int), np.array([], int), np.array([])
        return np.concatenate(out_p), np.concatenate(out_s), np.concatenate(out_d)
