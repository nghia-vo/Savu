# replaces tomobar_recon_yaml.py
from savu.plugins.plugin_info import PluginInfo

class TomoBarReconInfo(PluginInfo):
    """
    .. module:: tomobar_recon
       :platform: Unix
       :synopsis: A wrapper around TOmographic MOdel-BAsed Reconstruction \
         (ToMoBAR) software for advanced iterative image reconstruction
    .. moduleauthor:: Daniil Kazantsev <scientificsoftware@diamond.ac.uk>
    """
    def define_parameters(self):
        """---
        output_size:
            visibility: advanced
            dtype: Union[int, tuple]
            description: Number of rows and columns in the reconstruction.
            default: auto

        data_fidelity:
            visibility: advanced
            dtype: str
            description: Least Squares only at the moment.
            default: LS

        data_Huber_thresh:
            visibility: advanced
            dtype: int
            description: Threshold parameter for __Huber__ data fidelity.
            default: None

        data_any_rings:
            visibility: advanced
            dtype: int
            description: a parameter to suppress various artifacts including
              rings and streaks
            default: None

        data_any_rings_winsizes:
           visibility: advanced
           dtype: tuple
           description: half window sizes to collect background information
             [detector, angles, num of projections]
           default: (9,7,0)

        data_any_rings_power:
            visibility: advanced
            dtype: float
            description: a power parameter for Huber model.
            default: 1.4

        data_full_ring_GH:
             visibility: param
             dtype: str
             description: Regularisation variable for full constant ring removal (GH model).
             default: None

        data_full_ring_accelerator_GH:
             visibility: param
             dtype: float
             description: Acceleration constant for GH ring removal. (use with care)
             default: 10

        algorithm_iterations:
             visibility: param
             dtype: int
             description:
               summary: Number of outer iterations for FISTA (default)or ADMM methods.
               verbose: Less than 10 iterations for the iterative method
                  (FISTA) can deliver a blurry reconstruction. The
                  suggested value is 15 iterations, however the
                  algorithm can stop prematurely based on the tolerance
                  value.
             default: 20

        algorithm_verbose:
             visibility: param
             dtype: str
             description: print iterations number and other messages (off by default).
             default: 'off'

        algorithm_ordersubsets:
             visibility: param
             dtype: int
             description: The number of ordered-subsets to accelerate reconstruction.
             default: 6

        regularisation_method:
             visibility: param
             dtype: str
             options: [ROF_TV, FGP_TV, PD_TV, SB_TV, LLT_ROF, NDF, Diff4th]
             description:
               summary: The denoising method
               verbose: Iterative methods can help to solve ill-posed
                          inverse problems by choosing a suitable noise
                          model for the measurement
               options:
                   ROF_TV: Rudin-Osher-Fatemi Total Variation model
                   FGP_TV: Fast Gradient Projection Total Variation model
                   PD_TV: Primal-Dual Total Variation
                   SB_TV: Split Bregman Total Variation model
                   LLT_ROF: Lysaker, Lundervold and Tai model combined
                     with Rudin-Osher-Fatemi
                   NDF: Nonlinear/Linear Diffusion model (Perona-Malik,
                     Huber or Tukey)
                   DIFF4th: Fourth-order nonlinear diffusion model
             default: PD_TV

        regularisation_parameter:
             visibility: param
             dtype: float
             description:
               summary: Regularisation parameter. The higher the value, the
                 stronger the smoothing effect
               range: Recommended between 0 and 1
             default: 0.0001

        regularisation_iterations:
             visibility: param
             dtype: int
             description: The number of regularisation iterations.
             default: 80

        regularisation_device:
             visibility: param
             dtype: str
             description: The number of regularisation iterations.
             default: gpu

        regularisation_PD_lip:
             visibility: param
             dtype: int
             description: Primal-dual parameter for convergence.
             default: 8
             dependency:
               regularisation_method: PD_TV

        regularisation_methodTV:
             visibility: param
             dtype: str
             description: 0/1 - TV specific isotropic/anisotropic choice.
             default: 0
             dependency:
               regularisation_method: [ROF_TV, FGP_TV, SB_TV, NLTV]

        regularisation_timestep:
             visibility: param
             dtype: float
             dependency:
               regularisation_method: [ROF_TV, LLT_ROF, NDF, Diff4th]
             description:
               summary: Time marching parameter
               range: Recommended between 0.0001 and 0.003
             default: 0.003

        regularisation_edge_thresh:
             visibility: param
             dtype: float
             dependency:
               regularisation_method: [NDF, Diff4th]
             description:
               summary: Edge (noise) related parameter
             default: 0.01

        regularisation_parameter2:
             visibility: param
             dtype: float
             dependency:
               regularisation_method: LLT_ROF
             description:
               summary: Regularisation (smoothing) value
               verbose: The higher the value stronger the smoothing effect
             default: 0.005

        NDF_penalty:
             visibility: param
             dtype: str
             options: [Huber, Perona, Tukey]
             description:
               summary: Penalty dtype
               verbose: Nonlinear/Linear Diffusion model (NDF) specific penalty
                 type.
               options:
                 Huber: Huber
                 Perona: Perona-Malik model
                 Tukey: Tukey
             dependency:
               regularisation_method: NDF
             default: Huber

        max_iterations:
             visibility: param
             dtype: int
             description:
               summary: Total number of regularisation iterations.
                 The smaller the number of iterations, the smaller the effect
                 of the filtering is. A larger number will affect the speed
                 of the algorithm.
               range: Recommended value dependent upon method.
             default:
                 regularisation_method:
                   ROF_TV: 1000
                   FGP_TV: 500
                   PD_TV: 100
                   SB_TV: 100
                   LLT_ROF: 1000
                   NDF: 1000
                   DIFF4th: 1000
        """


    def get_bibtex(self):
        """@article{beck2009fast,
         title={A fast iterative shrinkage-thresholding algorithm for linear inverse problems},
         author={Beck, Amir and Teboulle, Marc},
         journal={SIAM journal on imaging sciences},
         volume={2},
         number={1},
         pages={183--202},
         year={2009},
         publisher={SIAM}
        }
        """


    def get_endnote(self):
        """%0 Journal Article
        %T A fast iterative shrinkage-thresholding algorithm for linear inverse problems
        %A Beck, Amir
        %A Teboulle, Marc
        %J SIAM journal on imaging sciences
        %V 2
        %N 1
        %P 183-202
        %@ 1936-4954
        %D 2009
        %I SIAM
        """

