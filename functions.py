def destaque_max_min(s):

    is_max = s == s.max()
    is_min = s == s.min()
    return ['background-color: green' if v else 'background-color: red' if m else '' for v, m in zip(is_max, is_min)]