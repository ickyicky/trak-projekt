import numpy as np
from PIL import Image
import cv2 as cv
import argparse


def getPSNR(I1, I2):
    s1 = cv.absdiff(I1, I2)  # |I1 - I2|
    s1 = np.float32(s1)  # cannot make a square on 8 bits
    s1 = s1 * s1  # |I1 - I2|^2
    sse = s1.sum()  # sum elements per channel
    if sse <= 1e-10:  # sum channels
        return 0  # for small values return zero
    else:
        shape = I1.shape
        mse = 1.0 * sse / (shape[0] * shape[1] * shape[2])
        psnr = 10.0 * np.log10((255 * 255) / mse)
        return psnr


def getMSSISM(i1, i2):
    C1 = 6.5025
    C2 = 58.5225
    # INITS
    I1 = np.float32(i1)  # cannot calculate on one byte large values
    I2 = np.float32(i2)
    I2_2 = I2 * I2  # I2^2
    I1_2 = I1 * I1  # I1^2
    I1_I2 = I1 * I2  # I1 * I2
    # END INITS
    # PRELIMINARY COMPUTING
    mu1 = cv.GaussianBlur(I1, (11, 11), 1.5)
    mu2 = cv.GaussianBlur(I2, (11, 11), 1.5)
    mu1_2 = mu1 * mu1
    mu2_2 = mu2 * mu2
    mu1_mu2 = mu1 * mu2
    sigma1_2 = cv.GaussianBlur(I1_2, (11, 11), 1.5)
    sigma1_2 -= mu1_2
    sigma2_2 = cv.GaussianBlur(I2_2, (11, 11), 1.5)
    sigma2_2 -= mu2_2
    sigma12 = cv.GaussianBlur(I1_I2, (11, 11), 1.5)
    sigma12 -= mu1_mu2
    t1 = 2 * mu1_mu2 + C1
    t2 = 2 * sigma12 + C2
    t3 = t1 * t2  # t3 = ((2*mu1_mu2 + C1).*(2*sigma12 + C2))
    t1 = mu1_2 + mu2_2 + C1
    t2 = sigma1_2 + sigma2_2 + C2
    t1 = t1 * t2  # t1 =((mu1_2 + mu2_2 + C1).*(sigma1_2 + sigma2_2 + C2))
    ssim_map = cv.divide(t3, t1)  # ssim_map =  t3./t1;
    mssim = cv.mean(ssim_map)  # mssim = average of ssim map
    return mssim


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("reference", type=str, help="Path to reference image")
    parser.add_argument(
        "undertest",
        type=str,
        help="Path to the image to be tested",
    )
    args = parser.parse_args()

    psnrv = 0.0
    mssism = 0.0

    with Image.open(args.reference) as ref:
        with Image.open(args.undertest) as utest:
            ref = np.array(ref)
            utest = np.array(utest)
            psnrv = getPSNR(ref, utest)
            mssism = getMSSISM(ref, utest)

    print(f"PSNRV: {psnrv:.4f}")
    print(f"MSSISM: R {mssism[2]:.2%} G {mssism[1]:.2%} B {mssism[0]:.2%}")


if __name__ == "__main__":
    main()
