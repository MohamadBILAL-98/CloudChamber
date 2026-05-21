# compareSimulationData.py
import sys
sys.path.insert(1, "../")
import numpy as np
import pickle
import matplotlib.pyplot as plt

from cloudChamberCommonCode import my_logger
from cloudChamberCommonCode import rawDataDirectory
from cloudChamberCommonCode import calibrationFactor
from cloudChamberCommonCode import goodCluster
from cloudChamberCommonCode import minLength
from cloudChamberCommonCode import maxLength
from cloudChamberCommonCode import coronaSize
from cloudChamberCommonCode import interestArea_x1
from cloudChamberCommonCode import interestArea_y1
from cloudChamberCommonCode import interestArea_x2
from cloudChamberCommonCode import interestArea_y2

def main():

    # ── Load real data ────────────────────────────────────────────
    clusterFile = open(rawDataDirectory + "MergedNoncorrelatedClusterData.dat", "rb")
    clusterDict = pickle.load(clusterFile)
    clusterFile.close()

    # ── Fiducial cuts ─────────────────────────────────────────────
    fiduX1 = coronaSize / calibrationFactor
    fiduX2 = (interestArea_x2 - interestArea_x1) - coronaSize / calibrationFactor
    fiduY1 = coronaSize / calibrationFactor
    fiduY2 = (interestArea_y2 - interestArea_y1) - coronaSize / calibrationFactor

    # ── Build real data length distribution ───────────────────────
    realLengthDistribution = np.empty(0, dtype=float)
    for iImage, clusterList in clusterDict.items():
        for cluster in clusterList:
            if (goodCluster(cluster) and
                    2.0*calibrationFactor*cluster[5] > minLength and
                    2.0*calibrationFactor*cluster[5] < maxLength):
                if (cluster[2]>fiduX1 and cluster[2]<fiduX2 and
                        cluster[3]>fiduY1 and cluster[3]<fiduY2):
                    realLengthDistribution = np.append(
                        realLengthDistribution,
                        2.0*calibrationFactor*cluster[5]
                    )

    my_logger.info("Real data: %d tracks" % len(realLengthDistribution))

    # ── Load simulation results for each Lz ──────────────────────
    lzValues = [30, 60, 100, 150]
    colors   = ['red', 'green', 'orange', 'purple']
    simData  = {}

    for lz in lzValues:
        fileName = '../../data/simulationResults_Lz%dmm.pkl' % lz
        try:
            with open(fileName, 'rb') as f:
                simData[lz] = pickle.load(f)
            my_logger.info("Loaded simulation Lz=%dmm: %d tracks seen"
                          % (lz, simData[lz]['trackNumberSeen']))
        except:
            my_logger.warning("File not found: %s" % fileName)

    # ── Plot comparison ───────────────────────────────────────────
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(12, 7))

    # bin definition
    binWidth    = 1.0
    lengthValues = np.arange(10., 100. + binWidth, binWidth)
    lengthValuesCenter = np.array([
        0.5*(lengthValues[i]+lengthValues[i+1])
        for i in range(len(lengthValues)-1)
    ])

    # ── Real data histogram ───────────────────────────────────────
    histoReal, _, _ = ax.hist(
        realLengthDistribution,
        bins=lengthValues,
        log=True,
        color='blue',
        alpha=0.6,
        label='Données réelles (%d traces)' % len(realLengthDistribution)
    )

    # ── Simulation histograms overlaid ────────────────────────────
    for lz, color in zip(lzValues, colors):
        if lz not in simData:
            continue

        simLength = simData[lz]['lengthDistribution']
        simLength = simLength[(simLength > minLength) & (simLength < maxLength)]

        # normalize simulation to same number of entries as real data
        normFactor = len(realLengthDistribution) / len(simLength) if len(simLength) > 0 else 1.

        ax.hist(
            simLength,
            bins=lengthValues,
            log=True,
            histtype='step',
            color=color,
            linewidth=2,
            weights=np.ones(len(simLength)) * normFactor,
            label='Simulation Lz=%dmm (%d traces vues)' % (lz, simData[lz]['trackNumberSeen'])
        )

    ax.set_yscale('log')
    ax.set_xlim(0., 100.)
    ax.set_ylim(0.1, 10000.)
    ax.set_xlabel(r"$\rm{Longueur \; de \; trace \; l \; (mm)}$", fontsize=14)
    ax.set_ylabel(r"$\rm{dN/dl \; (mm)}$", fontsize=14)
    ax.set_title(r"$\rm{Comparaison \; données \; réelles \; vs \; simulation}$", fontsize=14)
    ax.legend(fontsize=11)

    plt.tight_layout()
    plt.savefig(rawDataDirectory + "comparison_simulation_data.pdf")
    my_logger.info("Comparison plot saved")
    plt.show()

    # ── Print summary table ───────────────────────────────────────
    my_logger.info("=" * 60)
    my_logger.info("SUMMARY — Effect of activeVolumeHeight on efficiency")
    my_logger.info("=" * 60)
    my_logger.info("Real data tracks: %d" % len(realLengthDistribution))
    my_logger.info("-" * 60)

    fiducialArea = (fiduY2-fiduY1)*(fiduX2-fiduX1) * calibrationFactor**2 / 1.e6
    clusterRate  = 0.2855  # per second
    clusterRateError = 0.0063

    for lz in lzValues:
        if lz not in simData:
            continue
        efficiency = simData[lz]['trackNumberSeen'] / simData[lz]['trackNumber']
        Vfiducial  = fiducialArea * lz / 1000.  # m³
        activity   = clusterRate / (efficiency * Vfiducial * 3.)
        activityError = clusterRateError / (efficiency * Vfiducial * 3.)
        my_logger.info("Lz=%3dmm | efficiency=%5.2f%% | V=%8.2e m3 | Activity=%6.1f +- %4.1f Bq/m3"
                      % (lz, efficiency*100., Vfiducial, activity, activityError))

    my_logger.info("=" * 60)

if __name__ == "__main__":
    rc = main()
    sys.exit(rc)