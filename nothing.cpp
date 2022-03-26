MPI_Allreduce(biasCountsIn.data(), biasCounts.data(), 
              numSimulations, MPI_INT, MPI_SUM, simulationMastersComm);
