import argparse
import networkx as nx
import trailmap.parse_input as pi
import trailmap.commodity_dictionary as cd
import trailmap.acquisition_paths as ap
import trailmap.pathway_analysis as pa
import networkx as nx
from pprint import pprint
import matplotlib.pyplot as plt


def make_parser():
    """Makes the Cyclus-Trailmap command line parser"""
    p = argparse.ArgumentParser(description="Cyclus-Trailmap command line",
                                epilog="python main.py cyclus_input_file.xml")
    p.add_argument('infile', nargs=1, help='Cyclus input file. Must be XML')
    p.add_argument('--draw', '-d', action='store_true')
    p.add_argument('--pickle', '-p', action='store_true',
                   help="pickle graph output of fuel cycle")
    p.add_argument('--pickle-file', dest='picklefile',
                   default='trailmap.gpickle',
                   help='output path for pickled graph')
    p.add_argument('--supress-print', '-sp', action='store_true')
    p.add_argument('--facility-search', '-f', nargs=3, required=False,
                   help='first argument is the name of the facility, second\
                   argument is whether the placement of the facility in the\
                   path matters. Acceptable values are any, start, and end.\
                   Third argument is draw or nodraw')
    p.add_argument('--connect-facilities', '-cf', nargs=2, required=False,
                   help='finds pathwas that begin at the first facility add\
                   end at the second')
    p.add_argument('--node-disjoint', '-nd', nargs=2,
                   help='returns a list of node disjoint paths between a\
                   source and target facility')

    return p


def main(args=None):
    """Main function for Cyclus-Trailmap CLI"""
    p = make_parser()
    ns = p.parse_args(args=args)

    commodity_dictionary = cd.build_commod_dictionary()
    (facility_dict_in,
    facility_dict_out) = pi.parse_input(ns.infile[0], commodity_dictionary)
    (G, pathways) = ap.conduct_apa(facility_dict_in, facility_dict_out)

    if ns.supress_print is False:
        ap.print_acquisition_paths(pathways)

    if ns.pickle:
        nx.write_gpickle(G, ns.picklefile)
    if ns.infile[0] is not None:
        commodity_dictionary = cd.build_commod_dictionary()
        (facility_dict_in,
         facility_dict_out) = pi.parse_input(ns.infile[0],
                                             commodity_dictionary)
        (G, pathways) = ap.conduct_apa(facility_dict_in,
                                       facility_dict_out)
        pa.print_graph_parameters(G, pathways)

        if ns.draw:
            plt = pa.draw_graph(G)
            plt.show()
        if ns.pickle:
            nx.write_gpickle(G, ns.picklefile)
        if ns.facility_search is not None:
            facility = str(ns.facility_search[0])
            location = str(ns.facility_search[1])
            print("\nPathways going through " + facility)
            fs_pathways = pa.find_facility_specific_paths(pathways, facility,
                                                          location)
            pprint(fs_pathways)
            if ns.facility_search[2] == 'draw':
                for path in [path for path in fs_pathways if ns.draw]:
                    pa.draw_path(G, path)
        if ns.node_disjoint is not None:
            source = str(ns.node_disjoint[0])
            target = str(ns.node_disjoint[1])
            print("\nNode Disjoint paths")
            ndp = pa.find_node_disjoint_paths(G, source, target)
            pprint(ndp)
        if ns.connect_facilities is not None:
            source = str(ns.connect_facilities[0])
            target = str(ns.connect_facilities[1])
            print('\nPathways between ' + source + ' and ' + target)
            paths = pa.find_paths_between_facilities(pathways, source, target)
            pprint(paths)

    else:
        print('No input file given!')


if __name__ == '__main__':
    main()
