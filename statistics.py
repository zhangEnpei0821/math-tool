"""统计学"""


__all__ = ['to_list', 'to_z_score', 'from_z_score','mean','median','mode', 'variance','standard_deviation', 'coefficient_of_dispersion',
          'standard_error', 'covariance', 'linear_regression','multiple_linear_regression', 'r_squared', 'coefficient_of_determination',
           'coefficient_of_variation', 'correlation_coefficient', 't_test', 'z_test', 'chi_squared_test', 'f_test']


def to_list(data):
    """将数据转换为列表"""
    if isinstance(data, list):
        return data
    elif isinstance(data, tuple):
        return list(data)
    elif isinstance(data, set):
        return list(data)
    elif isinstance(data, dict):
        result = []
        for k, v in data.items():
            for i in range(v):
                result.append(k)
        return result
    elif isinstance(data, str):
        return list(data)
    else:
        return [data]


def to_z_score(x, mean_value, standard_deviation):
    """将数据转换为标准分"""
    return (x - mean_value) / standard_deviation


def from_z_score(z, mean_value, standard_deviation):
    """将标准分转换为数据"""
    return z * standard_deviation + mean_value


def mean(data):
    """计算数据集的平均值"""
    return sum(data) / len(data)


def median(data):
    """计算数据集的中位数"""
    n = len(data)
    sorted_data = sorted(data)
    if n % 2 == 0:
        return (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2
    else:
        return sorted_data[n // 2]


def mode(data):
    """计算数据集的众数"""
    counts = {}
    for x in data:
        if x in counts:
            counts[x] += 1
        else:
            counts[x] = 1
    max_count = 0
    mode = None
    for x, count in counts.items():
        if count > max_count:
            max_count = count
            mode = x
    return mode


def variance(data):
    """计算数据集的方差"""
    n = len(data)
    mean_value = mean(data)
    return sum((x - mean_value) ** 2 for x in data) / n


def standard_deviation(data):
    """计算数据集的标准差"""
    return variance(data) ** 0.5


def coefficient_of_dispersion(data):
    """计算数据集的离散系数"""
    return standard_deviation(data) / mean(data)


def standard_error(data):
    """计算数据集的标准误差"""
    return standard_deviation(data) / len(data) ** 0.5


def covariance(x, y):
    """计算两个变量之间的协方差"""
    n = len(x)
    mean_x = mean(x)
    mean_y = mean(y)
    return sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / (n - 1)


def linear_regression(x, y):
    """计算线性回归方程"""
    n = len(x)
    mean_x = mean(x)
    mean_y = mean(y)
    cov_xy = covariance(x, y)
    var_x = variance(x)
    slope = cov_xy / var_x
    intercept = mean_y - slope * mean_x
    return lambda x: slope * x + intercept


def multiple_linear_regression(x, y, *args):
    """计算多元线性回归方程"""
    n = len(x)
    means = [mean(data) for data in [x, y] + list(args)]
    cov_matrix = [[covariance(x, y), covariance(x, z)] for x, y, z in zip(x, y, *args)]
    var_x = variance(x)
    var_y = variance(y)
    var_z = [variance(z) for z in args]
    cov_xy = covariance(x, y)
    cov_xz = [covariance(x, z) for z in args]
    cov_yz = [covariance(y, z) for z in args]
    cov_xyz = [covariance(x, y, z) for z in args]
    var_xyz = [variance(x, y, z) for z in args]
    a = cov_xy / var_x
    b = cov_xz / var_x
    c = cov_yz / var_y
    d = cov_xyz / var_x
    e = cov_xyz / var_y
    f = cov_xyz / var_z
    g = var_xyz / (var_x * var_y * var_z)
    h = [mean_y - a * mean_x - b[i] * means[0] - c[i] * means[1] for i in range(len(args))]
    return lambda x, y, *args: a * x + b[0] * y + c[0] * args[0] + d[0] * x * y + e[0] * y * args[0] + f[0] * x * args[0] + g[0] * x * y * args[0] + h[0]


def r_squared(data, regression_line):
    """计算回归线与数据集之间的平方和"""
    n = len(data)
    y_mean = mean(data)
    ss_tot = sum((y - y_mean) ** 2 for y in data)
    ss_res = sum((y - regression_line(x)) ** 2 for x, y in zip(range(n), data))
    return 1 - ss_res / ss_tot


def coefficient_of_determination(data, regression_line):
    """计算回归线与数据集之间的相关系数"""
    n = len(data)
    y_mean = mean(data)
    ss_tot = sum((y - y_mean) ** 2 for y in data)
    ss_res = sum((y - regression_line(x)) ** 2 for x, y in zip(range(n), data))
    return 1 - ss_res / ss_tot


def coefficient_of_variation(data):
    """计算数据集的变异系数"""
    return standard_deviation(data) / mean(data)


def correlation_coefficient(x, y):
    """计算两个变量之间的相关系数"""
    n = len(x)
    mean_x = mean(x)
    mean_y = mean(y)
    cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
    var_x = variance(x)
    var_y = variance(y)
    return cov / (var_x * var_y) ** 0.5


def t_test(data1, data2):
    """计算两个数据集之间的t检验值"""
    n1 = len(data1)
    n2 = len(data2)
    mean1 = mean(data1)
    mean2 = mean(data2)
    var1 = variance(data1)
    var2 = variance(data2)
    std1 = standard_deviation(data1)
    std2 = standard_deviation(data2)
    t = (mean1 - mean2) / ((std1 ** 2 / n1 + std2 ** 2 / n2) ** 0.5)
    df = (var1 / n1 + var2 / n2) ** 2 / ((var1 ** 2 / (n1 - 1)) + (var2 ** 2 / (n2 - 1)))
    return t, df


def z_test(data1, data2):
    """计算两个数据集之间的z检验值"""
    n1 = len(data1)
    n2 = len(data2)
    mean1 = mean(data1)
    mean2 = mean(data2)
    std1 = standard_deviation(data1)
    std2 = standard_deviation(data2)
    z = (mean1 - mean2) / ((std1 / n1 ** 0.5 + std2 / n2 ** 0.5) ** 0.5)
    return z


def chi_squared_test(data):
    """计算卡方检验值"""
    n = len(data)
    counts = {}
    for x in data:
        if x in counts:
            counts[x] += 1
        else:
            counts[x] = 1
    expected = [n * counts[x] / sum(counts.values()) for x in counts]
    chi_squared = sum((counts[x] - expected[i]) ** 2 / expected[i] for i, x in enumerate(counts))
    df = len(counts) - 1
    return chi_squared, df


def f_test(data1, data2):
    """计算方差分析表"""
    n1 = len(data1)
    n2 = len(data2)
    mean1 = mean(data1)
    mean2 = mean(data2)
    var1 = variance(data1)
    var2 = variance(data2)
    std1 = standard_deviation(data1)
    std2 = standard_deviation(data2)
    f = (var1 / n1 + var2 / n2) / (std1 ** 2 / n1 + std2 ** 2 / n2)
    df1 = n1 - 1
    df2 = n2 - 1
    return f, df1, df2


def anova_test(data1, data2, data3, *args):
    """计算方差分析表"""
    n1 = len(data1)
    n2 = len(data2)
    n3 = len(data3)
    means = [mean(data) for data in [data1, data2, data3] + list(args)]
    variances = [variance(data) for data in [data1, data2, data3] + list(args)]
    stds = [standard_deviation(data) for data in [data1, data2, data3] + list(args)]
    ssb = sum((n * (mean - means[0]) ** 2 for n, mean in zip([n1, n2, n3] + [len(data) for data in args], means)))
    ssw = sum((n - 1) * variance for n, variance in zip([n1, n2, n3] + [len(data) for data in args], variances))
    sst = ssb + ssw
    dfw = len(means) - 1
    dfb = n1 + n2 + n3 - len(means)
    msb = ssb / dfb
    msw = ssw / dfw
    f = msb / msw
    return f, dfb, dfw


def t_test_paired(data1, data2):
    """计算配对样本t检验值"""
    n = len(data1)
    mean1 = mean(data1)
    mean2 = mean(data2)
    var1 = variance(data1)
    var2 = variance(data2)
    std1 = standard_deviation(data1)
    std2 = standard_deviation(data2)
    t = (mean1 - mean2) / ((std1 ** 2 / n + std2 ** 2 / n) ** 0.5)
    df = n - 1
    return t, df


def z_test_paired(data1, data2):
    """计算配对样本z检验值"""
    n = len(data1)
    mean1 = mean(data1)
    mean2 = mean(data2)
    std1 = standard_deviation(data1)
    std2 = standard_deviation(data2)
    z = (mean1 - mean2) / ((std1 / n ** 0.5 + std2 / n ** 0.5) ** 0.5)
    return z


def correlation_test(data1, data2):
    """计算相关性检验值"""
    n = len(data1)
    mean1 = mean(data1)
    mean2 = mean(data2)
    var1 = variance(data1)
    var2 = variance(data2)
    cov = sum((data1[i] - mean1) * (data2[i] - mean2) for i in range(n)) / n
    std1 = standard_deviation(data1)
    std2 = standard_deviation(data2)
    r = cov / (std1 * std2)
    df = n - 2
    return r, df


def mann_whitney_u_test(data1, data2):
    """计算曼-威廉斯U检验值"""
    n1 = len(data1)
    n2 = len(data2)
    rank1 = sorted(data1)
    rank2 = sorted(data2)
    rank_sum = sum(i * (n1 - i + 1) for i in range(1, n1 + 1)) + sum(i * (n2 - i + 1) for i in range(1, n2 + 1))
    u = n1 * n2 + (n1 * (n1 + 1)) / 2.0 - rank_sum
    return u


def kruskal_wallis_h_test(data1, data2, data3, *args):
    """计算克鲁斯金-WALLIS H检验值"""
    n1 = len(data1)
    n2 = len(data2)
    n3 = len(data3)
    n_total = n1 + n2 + n3 + sum(len(data) for data in args)
    rank_sum = sum(i * (n_total - i + 1) for i in range(1, n_total + 1))
    h = (12.0 / (n_total * (n_total + 1))) * (
        (n1 * (n2 + n3 + sum(len(data) for data in args)) - rank_sum) ** 2
        / (n1 * n2 * n3 * (n1 + n2 + n3 + sum(len(data) for data in args)))
    )
    return h


def friedman_test(data1, data2, data3, *args):
    """计算费雷德曼检验值"""
    n1 = len(data1)
    n2 = len(data2)
    n3 = len(data3)
    n_total = n1 + n2 + n3 + sum(len(data) for data in args)
    rank_sum = sum(i * (n_total - i + 1) for i in range(1, n_total + 1))
    f = (
        (n1 * n2 * n3) ** 0.5
        * (1 + (12.0 / (n_total * (n_total + 1))) * (rank_sum - 3 * (n1 + n2 + n3 + sum(len(data) for data in args))))
    )
    return f


def levene_test(data1, data2, data3, *args):
    """计算韦尔森-斯皮尔逊检验值"""
    n1 = len(data1)
    n2 = len(data2)
    n3 = len(data3)
    n_total = n1 + n2 + n3 + sum(len(data) for data in args)
    variances = [variance(data) for data in [data1, data2, data3] + list(args)]
    stds = [standard_deviation(data) for data in [data1, data2, data3] + list(args)]
    ssw = sum((n - 1) * variance for n, variance in zip([n1, n2, n3] + [len(data) for data in args], variances))
    ssbn = sum((n * (mean - means[0]) ** 2 for n, mean in zip([n1, n2, n3] + [len(data) for data in args], means)))
    ssb = ssbn - (n_total - 1) * ssw / n_total
    dfw = len(means) - 1
    dfbn = n1 + n2 + n3 + sum(len(data) for data in args) - len(means)
    dfb = dfbn - 1
    msb = ssb / dfb
    msw = ssw / dfw
    f = msb / msw
    return f, dfb, dfw


def wilcoxon_signed_rank_test(data1, data2):
    """计算威尔科克森-秩检验值"""
    n1 = len(data1)
    n2 = len(data2)
    rank1 = sorted(data1)
    rank2 = sorted(data2)
    rank_sum = sum(i * (n1 - i + 1) for i in range(1, n1 + 1)) + sum(i * (n2 - i + 1) for i in range(1, n2 + 1))
    u = n1 * n2 + (n1 * (n1 + 1)) / 2.0 - rank_sum
    t = u / (2 * (n1 * n2 * (n1 + n2 + 1)) ** 0.5)
    return t


def wilcoxon_rank_sum_test(data1, data2):
    """计算威尔科克森-秩和检验值"""
    n1 = len(data1)
    n2 = len(data2)
    rank1 = sorted(data1)
    rank2 = sorted(data2)
    rank_sum = sum(i * (n1 - i + 1) for i in range(1, n1 + 1)) + sum(i * (n2 - i + 1) for i in range(1, n2 + 1))
    u = n1 * n2 + (n1 * (n1 + 1)) / 2.0 - rank_sum
    z = u / (2 * (n1 + n2)) ** 0.5
    return z


def friedman_aligned_ranks_test(data1, data2, data3, *args):
    """计算费雷德曼对齐秩检验值"""
    n1 = len(data1)
    n2 = len(data2)
    n3 = len(data3)
    n_total = n1 + n2 + n3 + sum(len(data) for data in args)
    rank_sum = sum(i * (n_total - i + 1) for i in range(1, n_total + 1))
    f = (
        (n1 * n2 * n3) ** 0.5
        * (1 + (12.0 / (n_total * (n_total + 1))) * (rank_sum - 3 * (n1 + n2 + n3 + sum(len(data) for data in args))))
    )
    return f


def friedman_nemenyi_test(data1, data2, data3, *args):
    """计算费雷德曼尼曼检验值"""
    n1 = len(data1)
    n2 = len(data2)
    n3 = len(data3)
    n_total = n1 + n2 + n3 + sum(len(data) for data in args)
    rank_sum = sum(i * (n_total - i + 1) for i in range(1, n_total + 1))
    f = (
        (n1 * n2 * n3) ** 0.5
        * (1 + (12.0 / (n_total * (n_total + 1))) * (rank_sum - 3 * (n1 + n2 + n3 + sum(len(data) for data in args))))
    )
    return f


def friedman_chisquare_test(data1, data2, data3, *args):
    """计算费雷德曼卡方检验值"""
    n1 = len(data1)
    n2 = len(data2)
    n3 = len(data3)
    n_total = n1 + n2 + n3 + sum(len(data) for data in args)
    counts = {}
    for x in [data1, data2, data3] + list(args):
        for y in x:
            if y in counts:
                counts[y] += 1
            else:
                counts[y] = 1
    expected = [n_total * counts[x] / sum(counts.values()) for x in counts]
    chi_squared = sum((counts[x] - expected[i]) ** 2 / expected[i] for i, x in enumerate(counts))
    df = len(counts) - 1
    return chi_squared, df