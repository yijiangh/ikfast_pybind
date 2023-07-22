#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#ifndef IKFAST_HAS_LIBRARY
#define IKFAST_HAS_LIBRARY
#endif

#include "ikfast.h"

#ifdef IKFAST_NAMESPACE
using namespace IKFAST_NAMESPACE;
#endif

namespace py = pybind11;

PYBIND11_MODULE(ikfast_abb_crb15000_5_95, m)
{
    m.doc() = R"pbdoc(
        abb_crb15000_5_95
        -----------------------
        .. currentmodule:: abb_crb15000_5_95
        .. autosummary::
           :toctree: _generate
           get_ik
           get_fk
           get_dof
           get_free_dof
    )pbdoc";

    m.def("get_ik", [](const std::vector<double> &trans_list,
                       const std::vector<std::vector<double>> &rot_list,
                       const std::vector<double> &free_jt_vals)
    {
      using namespace ikfast;
      IkSolutionList<double> solutions;

      if (free_jt_vals.size() != GetNumFreeParameters()){
          return std::vector<std::vector<double>>();
      }

      double eerot[9], eetrans[3];
      for(std::size_t i = 0; i < 3; ++i) {
          eetrans[i] = trans_list[i];
          std::vector<double> rot_vec = rot_list[i];
          for(std::size_t j = 0; j < 3; ++j)
          {
              eerot[3*i + j] = rot_vec[j];
          }
      }

      // call ikfast routine
      bool b_success = ComputeIk(eetrans, eerot, &free_jt_vals[0], solutions);

      std::vector<std::vector<double>> solution_list;
      if (!b_success)
      {
          //fprintf(stderr,"Failed to get ik solution\n");
          return solution_list; // Equivalent to returning None in python
      }

      std::vector<double> solvalues(GetNumJoints());

      // convert all ikfast solutions into a std::vector
      for(std::size_t i = 0; i < solutions.GetNumSolutions(); ++i)
      {
          const IkSolutionBase<double>& sol = solutions.GetSolution(i);
          std::vector<double> vsolfree(sol.GetFree().size());
          sol.GetSolution(&solvalues[0],
                          vsolfree.size() > 0 ? &vsolfree[0] : NULL);

          std::vector<double> individual_solution = std::vector<double>(GetNumJoints());
          for(std::size_t j = 0; j < solvalues.size(); ++j)
          {
              individual_solution[j] = solvalues[j];
          }
          solution_list.push_back(individual_solution);
      }
      return solution_list;
    },
    py::arg("trans_list"),
    py::arg("rot_list"),
    py::arg("free_jt_vals"),
    R"pbdoc(
        get inverse kinematic solutions for abb_crb15000_5_95
    )pbdoc");

    m.def("get_fk", [](const std::vector<double> &joint_list)
    {
      using namespace ikfast;
      // eerot is a flattened 3x3 rotation matrix
      double eerot[9], eetrans[3];

      std::vector<double> joints(GetNumJoints());
      for(std::size_t i = 0; i < GetNumJoints(); ++i)
      {
          joints[i] = joint_list[i];
      }

      // call ikfast routine
      ComputeFk(&joints[0], eetrans, eerot);

      // convert computed EE pose to a python object
      std::vector<double> pos(3);
      std::vector<std::vector<double>> rot(3);

      for(std::size_t i = 0; i < 3; ++i)
      {
          pos[i] = eetrans[i];
          std::vector<double> rot_vec(3);
          for( std::size_t j = 0; j < 3; ++j)
          {
              rot_vec[j] = eerot[3*i + j];
          }
          rot[i] = rot_vec;
      }
      return std::make_tuple(pos, rot);
    },
    py::arg("joint_list"),
    R"pbdoc(
        get forward kinematic solutions for the abb_crb15000_5_95 robot
    )pbdoc");

    m.def("get_num_dofs", []()
    {
      return int(GetNumJoints());
    },
    R"pbdoc(
        get number of dofs configured for the ikfast module
    )pbdoc");

    m.def("get_free_dofs", []()
    {
        int* pindices = GetFreeParameters();
        // if pindices is NULL, then return an empty vector
        if (pindices == NULL)
        {
            return std::vector<int>();
        }
        else 
        {
            std::vector<int> indices(GetNumFreeParameters());
            for(std::size_t i = 0; i < GetNumFreeParameters(); ++i)
            {
                indices[i] = pindices[i];
            }
            return indices;
        }
    },
    R"pbdoc(
        get the indices of free dofs configured for the ikfast module
    )pbdoc");

#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif

}
