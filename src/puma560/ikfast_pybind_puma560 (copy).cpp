#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
// #include <pybind11/eigen.h>
// #include <pybind11/iostream.h>

#ifndef IKFAST_HAS_LIBRARY
#define IKFAST_HAS_LIBRARY
#endif

#include <puma560/ikfast.h>

#ifdef IKFAST_NAMESPACE
using namespace IKFAST_NAMESPACE;
#endif

namespace py = pybind11;

PYBIND11_MODULE(ikfast_puma560, m)
{
    m.doc() = R"pbdoc(
        ikfast_pybind_puma560
        -----------------------
        .. currentmodule:: ikfast_pybind_puma560
        .. autosummary::
           :toctree: _generate
           get_ik
           get_fk
    )pbdoc";

    m.def("get_ik", [](const std::vector<double> &trans_list,
                       const std::vector<std::vector<double>> &rot_list)
    {
      using namespace ikfast;
      IkSolutionList<double> solutions;

      std::vector<double> vfree(GetNumFreeParameters());
      double eerot[9], eetrans[3];
      if( rot_list.size() == 4 )  // ik, given translation vector and quaternion pose
      {
        eetrans[0] = trans_list[0];
        eetrans[1] = trans_list[1];
        eetrans[2] = trans_list[2];
        double qx = rot_list[0];
        double qy = rot_list[1];
        double qz = rot_list[2];
        double qw = rot_list[3];
        double n = 1.0f/sqrt(qx*qx+qy*qy+qz*qz+qw*qw);
        qw *= n;
        qx *= n;
        qy *= n;
        qz *= n;
        eerot[0] = 1.0f - 2.0f*qy*qy - 2.0f*qz*qz;  eerot[1] = 2.0f*qx*qy - 2.0f*qz*qw;         eerot[2] = 2.0f*qx*qz + 2.0f*qy*qw;
        eerot[3] = 2.0f*qx*qy + 2.0f*qz*qw;         eerot[4] = 1.0f - 2.0f*qx*qx - 2.0f*qz*qz;  eerot[5] = 2.0f*qy*qz - 2.0f*qx*qw;
        eerot[6] = 2.0f*qx*qz - 2.0f*qy*qw;         eerot[7] = 2.0f*qy*qz + 2.0f*qx*qw;         eerot[8] = 1.0f - 2.0f*qx*qx - 2.0f*qy*qy;
      }
      else if( rot_list.size() == 9 )   // ik, given rotation-translation matrix
      {
        eetrans[0] = trans_list[0];
        eetrans[1] = trans_list[1];
        eetrans[2] = trans_list[2];
        for(std::size_t i = 0; i < 9; ++i)
        {
          eerot[i] = rot_list[i];
        }
      }
      // call ikfast routine
      bool b_success = ComputeIk(eetrans, eerot, &vfree[0], solutions);

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
    R"pbdoc(
        get inverse kinematic solutions for pybind_puma560
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
        get forward kinematic solutions for kuka_kr6_r900
    )pbdoc");

    m.def("get_dof", []()
    {
      return int(GetNumJoints());
    },
    R"pbdoc(
        get number dofs configured for the ikfast module
    )pbdoc");

    m.def("get_free_dof", []()
    {
      return int(GetNumFreeParameters());
    },
    R"pbdoc(
        get number of free dofs configured for the ikfast module
    )pbdoc");

#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif

}
