### Recommended 
---
- Windows 10 Insider Preview Build 20246 or later
### Requirements
---
- WSL  
To make installing WSL as easily just by running one command: wsl --install
![wsl --install](https://devblogs.microsoft.com/commandline/wp-content/uploads/sites/33/2020/10/wslinstall.png)  
For more information please visit: https://devblogs.microsoft.com/commandline/distro-installation-added-to-wsl-install-in-windows-10-insiders-preview-build-20246/
- Python >= 3.7.6
### Interface
---
|file type   |option   |folder name   |filter output file   |filter output file index   |
|---|---|---|---|---|
|VCF file   |CPIC   |CPIC_Genes   |***FILE_NAME***_filtered_for_CPIC_genes.vcf.gz   |***FILE_NAME***_filtered_for_CPIC_genes.vcf.gz.tbi   |
|   |PGx   |PGX_Genes   |***FILE_NAME***_filtered_for_PGx_genes.vcf.gz   |***FILE_NAME***_filtered_for_PGx_genes.vcf.gz.tbi   |
|   |CPIC & PGx   |CPICandPGX_Genes   |***FILE_NAME***_filtered_for_CPIC_and_PGx_genes.vcf.gz   |***FILE_NAME***_filtered_for_CPIC_and_PGx_genes.vcf.gz.tbi   |
|BAM file   |HLA   |HLA_Genes   |***FILE_NAME***_filtered_for_HLA_genes.bam   |***FILE_NAME***_filtered_for_CYP2D6_genes.bam.bai   |
|   |CYP2D6   |CYP2D6_Genes   |***FILE_NAME***_filtered_for_CYP2D6_genes.bam   |***FILE_NAME***_filtered_for_CYP2D6_genes.bam.bai   |
|   |HLA & CYP2D6   |HLAandCYP2D6_Genes   |***FILE_NAME***_filtered_for_HLA_and_CYP2D6_genes.bam   |***FILE_NAME***_filtered_for_HLA_and_CYP2D6_genes.bam.bai   |
