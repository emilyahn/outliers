library(readr)

# Conduct logistic regression over all annotated samples

# load file: data/analysis/logreg_sibilants_all.csv
logreg_sibilants_all <- read_csv("data/analysis/logreg_sibilants_all.csv")

# ***** HAUSA as Lang2 (Kazakh as Lang1)

logreg_sibilants_all$Lang <- factor(logreg_sibilants_all$Lang, levels = c("kaz", "hau", "swe"))
contrasts(logreg_sibilants_all$Lang) <- contr.sum(3)
contrasts(logreg_sibilants_all$Lang)

logistic_model_interaction <- glm(deleted ~ v_high + Lang, data = logreg_sibilants_all, family = "binomial")
summary(logistic_model_interaction)
# Call:
#   glm(formula = deleted ~ v_high + Lang, family = "binomial", data = logreg_sibilants_all)
#
# Deviance Residuals:
#   Min       1Q   Median       3Q      Max
# -0.6930  -0.4165  -0.3234  -0.1885   2.8422
#
# Coefficients:
#   Estimate Std. Error z value Pr(>|z|)
# (Intercept)  -2.7389     0.1617 -16.935  < 2e-16 ***
#   v_high        0.5484     0.1412   3.884 0.000103 ***
#   Lang1         0.8864     0.1897   4.672 2.98e-06 ***
#   Lang2        -0.7340     0.2544  -2.885 0.003914 **
#   ---
#   Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1
#
# (Dispersion parameter for binomial family taken to be 1)
#
# Null deviance: 432.30  on 839  degrees of freedom
# Residual deviance: 391.57  on 836  degrees of freedom
# AIC: 399.57
#
# Number of Fisher Scoring iterations: 6



# ***** SWEDISH as Lang2 (Kazakh still as Lang1)

logreg_sibilants_all$Lang <- factor(logreg_sibilants_all$Lang, levels = c("kaz", "swe", "hau"))
contrasts(logreg_sibilants_all$Lang) <- contr.sum(3)
contrasts(logreg_sibilants_all$Lang)
logistic_model_interaction <- glm(deleted ~ v_high + Lang, data = logreg_sibilants_all, family = "binomial")
summary(logistic_model_interaction)
# Call:
#   glm(formula = deleted ~ v_high + Lang, family = "binomial", data = logreg_sibilants_all)
#
# Deviance Residuals:
#   Min       1Q   Median       3Q      Max
# -0.6930  -0.4165  -0.3234  -0.1885   2.8422
#
# Coefficients:
#   Estimate Std. Error z value Pr(>|z|)
# (Intercept)  -2.7389     0.1617 -16.935  < 2e-16 ***
#   v_high        0.5484     0.1412   3.884 0.000103 ***
#   Lang1         0.8864     0.1897   4.672 2.98e-06 ***
#   Lang2        -0.1524     0.2313  -0.659 0.509918
# ---
#   Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1
#
# (Dispersion parameter for binomial family taken to be 1)
#
# Null deviance: 432.30  on 839  degrees of freedom
# Residual deviance: 391.57  on 836  degrees of freedom
# AIC: 399.57
#
# Number of Fisher Scoring iterations: 6

# Interaction not significant.
logistic_model_interaction <- glm(deleted ~ v_high + Lang + v_high*Lang, data = logreg_sibilants_all, family = "binomial")
summary(logistic_model_interaction)

# Call:
# glm(formula = deleted ~ v_high + Lang + v_high * Lang, family = "binomial",
#     data = logreg_sibilants_all)

# Deviance Residuals:
#     Min       1Q   Median       3Q      Max
# -0.6910  -0.4185  -0.3438  -0.1596   2.9562

# Coefficients:
#              Estimate Std. Error z value Pr(>|z|)
# (Intercept)  -2.77529    0.17620 -15.750  < 2e-16 ***
# v_high        0.58651    0.17620   3.329 0.000873 ***
# Lang1         0.92431    0.20482   4.513  6.4e-06 ***
# Lang2        -0.12173    0.24177  -0.503 0.614630
# v_high:Lang1 -0.04611    0.20482  -0.225 0.821894
# v_high:Lang2 -0.14623    0.24177  -0.605 0.545303
# ---
# Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

# (Dispersion parameter for binomial family taken to be 1)

#     Null deviance: 432.30  on 839  degrees of freedom
# Residual deviance: 391.07  on 834  degrees of freedom
# AIC: 403.07

# Number of Fisher Scoring iterations: 7



# ******* NO Lang variable, just v_high
logistic_model_interaction <- glm(deleted ~ v_high, data = logreg_sibilants_all, family = "binomial")
summary(logistic_model_interaction)
# Call:
#   glm(formula = deleted ~ v_high, family = "binomial", data = logreg_sibilants_all)
#
# Deviance Residuals:
#   Min       1Q   Median       3Q      Max
# -0.5033  -0.5033  -0.2982  -0.2982   2.5042
#
# Coefficients:
#   Estimate Std. Error z value Pr(>|z|)
# (Intercept)  -2.5466     0.1379 -18.461  < 2e-16 ***
#   v_high        0.5444     0.1379   3.947 7.93e-05 ***
#   ---
#   Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1
#
# (Dispersion parameter for binomial family taken to be 1)
#
# Null deviance: 432.30  on 839  degrees of freedom
# Residual deviance: 416.17  on 838  degrees of freedom
# AIC: 420.17
#
# Number of Fisher Scoring iterations: 5