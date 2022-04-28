# ----------------------------------------------------------------------------
# Copyright (c) 2022, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import os
from importlib_metadata import metadata
import pkg_resources

import qiime2

def _get_data_from_tests(path):
    return pkg_resources.resource_filename('q2_fmt.tests',
                                           os.path.join('data', path))


def alpha_md_factory():
    return qiime2.Metadata.load(
        _get_data_from_tests('sample_metadata_alpha_div.tsv'))

def beta_md_factory():
    return qiime2.Metadata.load(
        _get_data_from_tests('sample_metadata_donors.tsv'))

def alpha_div_factory():
    return qiime2.Artifact.import_data(
        'SampleData[AlphaDiversity]', _get_data_from_tests('alpha_div.tsv'))

def beta_div_factory():
    return qiime2.Artifact.import_data(
        'DistanceMatrix', _get_data_from_tests('dist_matrix_donors.tsv'))


def group_timepoints_alpha_independent(use):
    alpha = use.init_artifact('alpha', alpha_div_factory)
    metadata = use.init_metadata('metadata', alpha_md_factory)

    timepoints, references = use.action(
        use.UsageAction('fmt', 'group_timepoints'),
        use.UsageInputs(
            diversity_measure=alpha,
            metadata=metadata,
            time_column='days_post_transplant',
            reference_column='relevant_donor',
            subject_column=False
        ),
        use.UsageOutputNames(
            timepoint_dists='timepoint_dists',
            reference_dists='reference_dists'
        )
    )

    timepoints.assert_output_type('GroupDist[Ordered, Independent]')
    references.assert_output_type('GroupDist[Unordered, Independent]')


def group_timepoints_beta(use):
    beta = use.init_artifact('beta', beta_div_factory)
    metadata = use.init_metadata('metadata', beta_md_factory)

    timepoints, references = use.action(
        use.UsageAction('fmt', 'group_timepoints'),
        use.UsageInputs(
            diversity_measure=beta,
            metadata=metadata,
            time_column='days_post_transplant',
            reference_column='relevant_donor',
            subject_column='subject',
        ),
        use.UsageOutputNames(
            timepoint_dists='timepoint_dists',
            reference_dists='reference_dists'
        )
    )

    timepoints.assert_output_type('GroupDist[Ordered, Matched]')
    references.assert_output_type('GroupDist[Unordered, Independent]')